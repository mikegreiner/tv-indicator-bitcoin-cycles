#!/usr/bin/env python3
"""
Pine Script Syntax Checker
Basic syntax validation for Pine Script files without requiring TradingView
"""

import re
import sys
from pathlib import Path

class PineSyntaxChecker:
    """
    Pine Script Syntax Checker

    This tool performs basic syntax validation for Pine Script files.
    Note: Pine Script semicolons are optional in most cases, so this checker
    only warns about potentially problematic patterns that might benefit
    from explicit semicolons for clarity and consistency.
    """
    def __init__(self):
        self.errors = []
        self.warnings = []

    def check_file(self, file_path):
        """Check a Pine Script file for basic syntax issues"""
        print(f"Checking {file_path}...")

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except FileNotFoundError:
            self.errors.append(f"File not found: {file_path}")
            return False
        except UnicodeDecodeError:
            self.errors.append(f"Encoding error in {file_path}")
            return False

        lines = content.split('\n')
        self.check_basic_syntax(content, lines)
        self.check_common_issues(content, lines)

        return len(self.errors) == 0

    def check_basic_syntax(self, content, lines):
        """Check for basic syntax errors"""
        # Check for matching brackets
        brackets = {'(': ')', '[': ']', '{': '}'}
        stack = []

        for i, line in enumerate(lines, 1):
            for char in line:
                if char in brackets:
                    stack.append((char, i))
                elif char in brackets.values():
                    if not stack:
                        self.errors.append(f"Line {i}: Unexpected closing bracket '{char}'")
                        continue
                    opening, open_line = stack.pop()
                    if brackets[opening] != char:
                        self.errors.append(f"Line {i}: Mismatched brackets. Opened '{opening}' on line {open_line}, closed '{char}' on line {i}")

        if stack:
            char, line = stack[-1]
            self.errors.append(f"Line {line}: Unclosed bracket '{char}'")

        # Check for basic Pine Script structure
        if not content.strip().startswith('//@version'):
            self.warnings.append("File should start with //@version directive")

        # Check Pine Script version
        version_match = re.search(r'//@version=(\d+)', content)
        if version_match:
            version = int(version_match.group(1))
            if version < 5:
                self.warnings.append(f"Pine Script version {version} is outdated. Consider upgrading to v6")
            elif version > 6:
                self.warnings.append(f"Pine Script version {version} is newer than expected. Ensure compatibility")
        else:
            self.warnings.append("Could not determine Pine Script version")

        # Check for indicator/strategy declaration
        if not re.search(r'(?:indicator|strategy)\s*\(', content):
            self.errors.append("No indicator or strategy declaration found")

        # Check for multiline comments (problematic in Pine Script)
        if '/*' in content or '*/' in content:
            self.errors.append("Multiline comments (/* ... */) detected. Use single-line comments (//) instead")

        # Check for problematic multiline constructs
        multiline_array_pattern = r'options=\s*\[[^\]]*\n'
        if re.search(multiline_array_pattern, content):
            self.errors.append("Multiline array in function call detected. Keep arrays on single line or use different formatting")

        # Check for other multiline function parameters that might cause issues
        multiline_param_pattern = r'\w+\([^)]*\n.*\w+.*\n.*[^)]*\)'
        if re.search(multiline_param_pattern, content):
            self.warnings.append("Complex multiline function call detected - verify syntax carefully")

        # Check for incomplete ternary operators (common syntax error)
        lines_list = content.split('\n')
        for i, line in enumerate(lines_list, 1):
            stripped = line.strip()
            # Check for ternary operator that ends with ? but no completion
            if stripped.endswith('?') and not stripped.count('?') == stripped.count(':'):
                # Look ahead to see if the ternary is completed on next lines
                if i < len(lines_list) - 1:
                    next_line = lines_list[i].strip()
                    if not (':' in next_line or '?' in next_line):
                        self.errors.append(f"Line {i}: Incomplete ternary operator. Ternary expressions should be completed with ':' and false value")

        # Check for multiline function calls with missing closing parentheses
        open_parens = 0
        multiline_start = 0
        in_multiline_call = False

        for i, line in enumerate(lines_list, 1):
            stripped = line.strip()

            # Skip comments and empty lines
            if stripped.startswith('//') or stripped == '':
                continue

            # Count parentheses
            for char in stripped:
                if char == '(':
                    open_parens += 1
                    if not in_multiline_call:
                        in_multiline_call = True
                        multiline_start = i
                elif char == ')':
                    open_parens -= 1

            # Check for multiline function calls that don't close properly
            if in_multiline_call and open_parens == 0:
                in_multiline_call = False
            elif in_multiline_call and i > multiline_start and open_parens > 0:
                # We're in a multiline call that hasn't closed yet
                continue
            elif in_multiline_call and open_parens < 0:
                self.errors.append(f"Line {i}: Extra closing parenthesis. Check multiline function call starting around line {multiline_start}")
                in_multiline_call = False
                open_parens = 0

        # Check if we ended with unclosed parentheses
        if open_parens > 0:
            self.errors.append(f"Line {len(lines_list)}: Unclosed parenthesis. Multiline function call starting around line {multiline_start} is missing closing parenthesis")

        # Check for reserved keywords used as variable names
        reserved_keywords = [
            'range', 'break', 'continue', 'delete', 'new', 'this', 'super',
            'class', 'interface', 'extends', 'implements', 'public', 'private',
            'protected', 'static', 'final', 'const', 'var', 'if', 'else', 'for',
            'while', 'switch', 'case', 'default', 'try', 'catch', 'throw',
            'return', 'function', 'method', 'property'
        ]

        for keyword in reserved_keywords:
            # Look for variable assignments using reserved keywords
            pattern = rf'\b{keyword}\s*='
            if re.search(pattern, content):
                self.errors.append(f"Reserved keyword '{keyword}' used as variable name. Choose a different name")

        # Check for invalid Pine Script data types
        invalid_types = [
            'int64', 'uint', 'uint8', 'uint16', 'uint32', 'uint64',
            'byte', 'double', 'char', r'string\[\]',
            'boolean', 'Integer', 'Float', 'String', 'Boolean'
        ]

        # Note: 'short' and 'long' are valid as strategy.direction constants

        for invalid_type in invalid_types:
            # Look for variable declarations using invalid types
            pattern = rf'\b{re.escape(invalid_type)}\b'
            if re.search(pattern, content):
                self.errors.append(f"Invalid Pine Script data type '{invalid_type}'. Use 'int', 'float', 'bool', 'string', 'color', or 'label' instead")

        # Check for global variable modification in functions (Pine Script scoping issue)
        global_vars = []
        for line in lines:
            stripped = line.strip()
            # Find global variable declarations
            if stripped.startswith('var ') and '=' in stripped:
                var_match = re.match(r'var\s+\w+\s+(\w+)\s*=', stripped)
                if var_match:
                    global_vars.append(var_match.group(1))
        

        # Check for modification of global variables within functions
        # Note: This is a simplified check that doesn't try to parse function boundaries
        # Pine Script function parsing is complex and error-prone in a static analyzer
        # For now, we'll skip this check to avoid false positives
        pass
                

        # Check for missing math. prefix on mathematical functions
        math_functions = [
            'sin', 'cos', 'tan', 'asin', 'acos', 'atan', 'sinh', 'cosh', 'tanh',
            'sqrt', 'log', 'log10', 'exp', 'pow', 'abs', 'round', 'ceil', 'floor',
            'max', 'min'
        ]

        for func in math_functions:
            # Look for function calls without math. prefix (but not in comments)
            pattern = rf'\b{func}\s*\('
            for i, line in enumerate(lines, 1):
                if pattern in line and not line.strip().startswith('//') and 'math.' + func not in line:
                    # Skip if it's a valid non-math function (like strategy.max)
                    if not re.search(r'\b(strategy|color|label|table|plot|fill)\.' + func, line):
                        self.warnings.append(f"Line {i}: Mathematical function '{func}()' should use 'math.{func}()' in Pine Script v6")

        # Check for str.format_time() type errors
        # str.format_time() expects series int (timestamp) but often gets series float
        for i, line in enumerate(lines, 1):
            if 'str.format_time(' in line and not line.strip().startswith('//'):
                # Look for common patterns that pass float to str.format_time
                if re.search(r'str\.format_time\s*\(\s*time\b', line):
                    self.warnings.append(f"Line {i}: str.format_time() may receive float timestamp from 'time'. Consider using math.round(time) to convert to int")
                elif re.search(r'str\.format_time\s*\(\s*[^,)]*time\[', line):
                    self.warnings.append(f"Line {i}: str.format_time() may receive float timestamp from 'time[]'. Consider using math.round() to convert to int")
                elif re.search(r'str\.format_time\s*\(\s*[^,)]*\)', line) and not re.search(r'str\.format_time\s*\(\s*math\.round\(', line):
                    # Check if the argument is not already wrapped in math.round()
                    self.warnings.append(f"Line {i}: str.format_time() expects series int (timestamp). Ensure argument is converted to int if needed")

        # Check for invalid plotting function parameters
        invalid_plot_params = [
            r'hline\([^,]+,[^,]+,[^,]+,.*linestyle',  # hline with linestyle parameter
            r'plot\([^,]+,[^,]+,.*linestyle',         # plot with linestyle parameter
            r'plotcandle\([^,]+,[^,]+,[^,]+,[^,]+,[^,]+,.*linestyle',  # plotcandle with linestyle
        ]

        for pattern in invalid_plot_params:
            for i, line in enumerate(lines, 1):
                if re.search(pattern, line) and not line.strip().startswith('//'):
                    self.errors.append(f"Line {i}: Invalid plotting function parameter. Remove 'linestyle' parameter - not supported in Pine Script v6")

        # Check for random.float() which doesn't exist in Pine Script
        for i, line in enumerate(lines, 1):
            if 'random.float(' in line and not line.strip().startswith('//'):
                self.errors.append(f"Line {i}: 'random.float()' is not available in Pine Script. Use deterministic alternatives like 'math.sin()' for testing")

        # Check for common Pine Script v6 migration issues
        v6_issues = [
            ('security(', 'request.security('),
            ('plotchar(', 'plotshape('),
            ('fill(', 'fill.new('),
            ('hline(', 'hline.new('),
        ]
        
        for old_func, new_func in v6_issues:
            for i, line in enumerate(lines, 1):
                if old_func in line and not line.strip().startswith('//'):
                    self.warnings.append(f"Line {i}: '{old_func}' may need to be updated to '{new_func}' for Pine Script v6 compatibility")

        # Check for potential array initialization issues
        array_operations = ['array.push', 'array.pop', 'array.get', 'array.set', 'array.size']
        has_array_ops = any(op in content for op in array_operations)
        if has_array_ops and 'array.new' not in content:
            self.warnings.append("Array operations detected but no array.new() initialization found")

        # Check for potential label/box/table initialization issues
        label_ops = ['label.new', 'label.delete', 'label.get_text', 'label.set_text']
        box_ops = ['box.new', 'box.delete', 'box.get_left', 'box.set_left']
        table_ops = ['table.new', 'table.delete', 'table.cell', 'table.set_cell']
        
        if any(op in content for op in label_ops) and 'var label' not in content:
            self.warnings.append("Label operations detected - ensure proper label variable declarations")
        
        if any(op in content for op in box_ops) and 'var box' not in content:
            self.warnings.append("Box operations detected - ensure proper box variable declarations")
            
        if any(op in content for op in table_ops) and 'var table' not in content:
            self.warnings.append("Table operations detected - ensure proper table variable declarations")

        # Check for potential strategy issues
        if 'strategy.entry' in content and 'strategy.exit' not in content:
            self.warnings.append("Strategy entries detected but no strategy exits found - check risk management")

        # Check for potential performance issues
        if 'for ' in content:
            loop_count = content.count('for ')
            if loop_count > 10:
                self.warnings.append(f"High number of loops detected ({loop_count}) - monitor performance and consider optimization")

        # Check for potential division by zero (only flag suspicious cases)
        suspicious_divisions = [
            r'/\s*\(\s*\w+\s*-\s*\w+\s*\)',  # division by subtraction (could be zero)
            r'/\s*\(\s*\w+\s*\+\s*\w+\s*\)',  # division by addition (less likely to be zero)
            r'/\s*\w+\s*$',  # division at end of line (might be incomplete)
        ]
        
        for pattern in suspicious_divisions:
            matches = re.finditer(pattern, content)
            for match in matches:
                line_num = content[:match.start()].count('\n') + 1
                self.warnings.append(f"Line {line_num}: Suspicious division operation detected - verify divisor cannot be zero")

        # Check for missing error handling in request.security calls
        if 'request.security' in content and 'na(' not in content:
            self.warnings.append("request.security() calls detected but no na() error handling found - consider adding error handling")

        # Check for common Pine Script patterns that might cause issues
        if 'var ' in content and 'label.new' in content:
            self.warnings.append("Global label variables detected - ensure labels are properly managed to avoid memory leaks")

        # Check for potential array bounds issues
        if 'array.get(' in content and 'array.size(' not in content:
            self.warnings.append("Array access operations detected - ensure proper bounds checking with array.size()")

        # Check for potential infinite loops
        loop_patterns = [
            r'for\s+\w+\s*=\s*\d+\s+to\s+\w+',  # for i = 0 to variable
            r'while\s+\w+\s*<',  # while condition
        ]
        
        for pattern in loop_patterns:
            if re.search(pattern, content):
                self.warnings.append("Loop with variable bounds detected - ensure termination conditions are met")

        # Check for duplicate variable declarations
        declared_vars = {}
        for i, line in enumerate(lines, 1):
            stripped = line.strip()
            if stripped and not stripped.startswith('//'):
                # Check for variable declarations
                if stripped.startswith('var '):
                    var_match = re.match(r'var\s+\w+\s+(\w+)\s*=', stripped)
                    if var_match:
                        var_name = var_match.group(1)
                        if var_name in declared_vars:
                            self.errors.append(f"Line {i}: Variable '{var_name}' is already defined on line {declared_vars[var_name]}")
                        else:
                            declared_vars[var_name] = i
                # Check for regular variable assignments (not declarations)
                elif re.match(r'^\s*\w+\s*[:=]', stripped) and not stripped.startswith('var '):
                    var_match = re.match(r'^\s*(\w+)\s*[:=]', stripped)
                    if var_match:
                        var_name = var_match.group(1)
                        if var_name in declared_vars:
                            # This is an assignment to an already declared variable, which is fine
                            pass
                        else:
                            # This is a new variable assignment
                            declared_vars[var_name] = i

        # Simple check for undeclared identifiers - only check specific known issues
        # This is a basic check for the most common Pine Script undeclared identifier errors
        # Skip function parameters as they are declared in function signatures
        common_undeclared_patterns = [
            (r'\bminCycleLength\b', 'minCycleLength'),
            (r'\bmaxCycleLength\b', 'maxCycleLength'),
            (r'\bcurrCycleBarCount\b', 'currCycleBarCount'),
            (r'\bcurrCycleLow\b', 'currCycleLow'),
            (r'\bcurrCycleHigh\b', 'currCycleHigh'),
        ]
        
        for i, line in enumerate(lines, 1):
            stripped = line.strip()
            if stripped and not stripped.startswith('//') and not stripped.startswith('//@'):
                # Skip function parameter checks - they are declared in function signatures
                if '=>' in stripped and re.match(r'^(\w+)\s*\([^)]*\)\s*=>', stripped):
                    continue
                    
                for pattern, var_name in common_undeclared_patterns:
                    if re.search(pattern, stripped):
                        # Check if this variable is declared before this line
                        declared_before = False
                        for j in range(i):
                            if re.search(rf'\b{var_name}\s*[:=]', lines[j]) or re.search(rf'\bvar\s+\w+\s+{var_name}\s*=', lines[j]):
                                declared_before = True
                                break
                        
                        if not declared_before:
                            self.errors.append(f"Line {i}: Undeclared identifier '{var_name}' - variable used before declaration")

        # Check for common Pine Script syntax issues
        # Check for missing parentheses in function calls
        for i, line in enumerate(lines, 1):
            stripped = line.strip()
            if stripped and not stripped.startswith('//'):
                # Check for function calls without parentheses
                if re.search(r'\b\w+\s*\([^)]*$', stripped) and not stripped.endswith(')'):
                    self.warnings.append(f"Line {i}: Potential incomplete function call - check parentheses")

        # Check for array access without proper syntax
        for i, line in enumerate(lines, 1):
            stripped = line.strip()
            if stripped and not stripped.startswith('//'):
                # Check for array access with wrong syntax
                if re.search(r'\w+\[\s*\w+\s*\]\s*=', stripped):
                    self.warnings.append(f"Line {i}: Array access syntax detected - ensure proper array operations")

        # Check for missing semicolons (only for problematic cases)
        problematic_patterns = [
            r'^\s*\w+\s*=.*\w+\s*\(.*\)\s*$',  # function calls in assignments
            r'^\s*\w+\s*:=.*\w+\s*\(.*\)\s*$',  # function calls in reassignments
            r'^\s*var\s+\w+.*=.*\w+\s*\(.*\)\s*$',  # var declarations with function calls
        ]

        for i, line in enumerate(lines, 1):
            stripped = line.strip()
            if (stripped and not stripped.startswith('//') and not stripped.startswith('//@') and
                not stripped.endswith(',') and not stripped.endswith('{') and not stripped.endswith('(') and
                not stripped.endswith('}') and not stripped.endswith(')') and not stripped.endswith(':') and
                not stripped.startswith('if') and not stripped.startswith('else') and not stripped.startswith('for')):

                # Only warn about potentially problematic cases
                for pattern in problematic_patterns:
                    if re.match(pattern, stripped):
                        self.warnings.append(f"Line {i}: Consider adding semicolon after function call: {stripped}")
                        break

    def check_common_issues(self, content, lines):
        """Check for common Pine Script issues"""
        # Get version for checks
        version_match = re.search(r'//@version=(\d+)', content)
        version = int(version_match.group(1)) if version_match else 5

        # Check for deprecated functions (Pine v5)
        deprecated_funcs = ['security', 'plotchar', 'fill']  # Some examples
        for func in deprecated_funcs:
            if f'{func}(' in content:
                self.warnings.append(f"Using potentially deprecated function: {func}")

        # Check for potential variable scoping issues
        var_declarations = re.findall(r'\bvar\s+\w+\s*=', content)
        for decl in var_declarations:
            self.warnings.append(f"Var declaration found: {decl.strip()} - ensure proper scoping")

        # Check for array usage without initialization
        array_usage = re.findall(r'\barray\.\w+', content)
        if array_usage and 'array.new' not in content:
            self.warnings.append("Array operations detected but no array initialization found")

        # Check for potential division by zero
        if '/' in content:
            self.warnings.append("Division operations found - check for potential division by zero")

        # Pine Script v6 specific checks
        if version >= 6:
            # Check for v6-specific features usage
            if 'request.security' in content:
                self.warnings.append("Using request.security - ensure proper error handling in v6")

            # Check for potential v6 migration issues
            if 'strategy.entry' in content and 'strategy.risk' not in content:
                self.warnings.append("Strategy entries detected - consider using strategy.risk for better risk management in v6")

            # Check for matrix usage (new in v6)
            if 'matrix.' in content:
                if 'matrix.new' not in content:
                    self.warnings.append("Matrix operations detected but no matrix initialization found")

        # General best practices
        if 'varip' in content or 'var()' in content:
            self.warnings.append("Using varip or var() for variable persistence - ensure proper scoping")

        if len(re.findall(r'\bif\s+\(', content)) > 10:
            self.warnings.append("High number of conditional statements - consider simplifying logic")

        # Check for large loops that might cause performance issues
        loop_count = len(re.findall(r'\bfor\s+', content))
        if loop_count > 5:
            self.warnings.append(f"High number of loops detected ({loop_count}) - monitor performance")

    def print_results(self):
        """Print the results of the syntax check"""
        if not self.errors and not self.warnings:
            print("✅ No issues found!")
            return

        if self.errors:
            print(f"\n❌ ERRORS ({len(self.errors)}):")
            for error in self.errors:
                print(f"  {error}")

        if self.warnings:
            print(f"\n⚠️  WARNINGS ({len(self.warnings)}):")
            for warning in self.warnings:
                print(f"  {warning}")

    def get_summary(self):
        """Get a summary of the results"""
        return {
            'errors': len(self.errors),
            'warnings': len(self.warnings),
            'passed': len(self.errors) == 0
        }

def main():
    if len(sys.argv) < 2:
        print("Usage: python pine-syntax-checker.py <pine_script_file>")
        print("Example: python pine-syntax-checker.py bitcoin-cycles-indicator.pine")
        sys.exit(1)

    file_path = sys.argv[1]

    if not Path(file_path).exists():
        print(f"❌ File not found: {file_path}")
        sys.exit(1)

    checker = PineSyntaxChecker()
    success = checker.check_file(file_path)
    checker.print_results()

    summary = checker.get_summary()
    if summary['passed']:
        print(f"\n✅ Syntax check passed! ({summary['warnings']} warnings)")
        sys.exit(0)
    else:
        print(f"\n❌ Syntax check failed! ({summary['errors']} errors, {summary['warnings']} warnings)")
        sys.exit(1)

if __name__ == "__main__":
    main()