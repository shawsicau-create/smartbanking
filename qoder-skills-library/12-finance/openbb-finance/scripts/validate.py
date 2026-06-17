"""
OpenBB Data Validation Script
Validates data quality and checks for common issues.
"""
import pandas as pd
from typing import Dict, List, Any


class DataValidator:
    """Validates financial data from OpenBB."""
    
    def __init__(self, df: pd.DataFrame):
        """
        Initialize validator with DataFrame.
        
        Args:
            df: Pandas DataFrame from OpenBB output
        """
        self.df = df
        self.issues = []
        self.warnings = []
    
    def validate_all(self) -> Dict[str, Any]:
        """
        Run all validation checks.
        
        Returns:
            Dictionary with validation results
        """
        print("=" * 60)
        print("OpenBB Data Validation Report")
        print("=" * 60)
        print()
        
        # Run all checks
        self._check_null_values()
        self._check_date_index()
        self._check_price_columns()
        self._check_negative_prices()
        self._check_duplicates()
        self._check_data_range()
        
        # Generate summary
        summary = self._generate_summary()
        
        return summary
    
    def _check_null_values(self):
        """Check for null values in DataFrame."""
        null_counts = self.df.isnull().sum()
        total_nulls = null_counts.sum()
        
        print("1. Null Value Check")
        print("-" * 40)
        
        if total_nulls == 0:
            print("✓ No null values found")
        else:
            print(f"⚠ Found {total_nulls} null values:")
            for column, count in null_counts[null_counts > 0].items():
                pct = (count / len(self.df)) * 100
                print(f"  - {column}: {count} ({pct:.1f}%)")
                self.warnings.append(f"Null values in {column}")
    
    def _check_date_index(self):
        """Check if DataFrame has proper datetime index."""
        print("\n2. Date Index Check")
        print("-" * 40)
        
        if not isinstance(self.df.index, pd.DatetimeIndex):
            print("⚠ Index is not a DatetimeIndex")
            self.issues.append("Index is not DatetimeIndex")
        else:
            print("✓ DatetimeIndex detected")
            
            # Check for missing dates
            date_range = pd.date_range(
                start=self.df.index.min(),
                end=self.df.index.max(),
                freq='D'
            )
            missing_dates = date_range.difference(self.df.index)
            
            if len(missing_dates) > 0:
                print(f"  Info: {len(missing_dates)} dates missing (likely weekends/holidays)")
            else:
                print("  Info: No missing dates in range")
    
    def _check_price_columns(self):
        """Check for required price columns."""
        print("\n3. Price Columns Check")
        print("-" * 40)
        
        required_columns = ['open', 'high', 'low', 'close', 'volume']
        missing_columns = [col for col in required_columns if col not in self.df.columns]
        
        if missing_columns:
            print(f"⚠ Missing required columns: {missing_columns}")
            self.issues.append(f"Missing columns: {missing_columns}")
        else:
            print(f"✓ All required columns present: {required_columns}")
    
    def _check_negative_prices(self):
        """Check for negative prices or volumes."""
        print("\n4. Negative Values Check")
        print("-" * 40)
        
        price_columns = [col for col in ['open', 'high', 'low', 'close'] if col in self.df.columns]
        has_negative = False
        
        for col in price_columns:
            negative_count = (self.df[col] < 0).sum()
            if negative_count > 0:
                print(f"⚠ {col}: Found {negative_count} negative values")
                self.issues.append(f"Negative values in {col}")
                has_negative = True
        
        if 'volume' in self.df.columns:
            negative_volume = (self.df['volume'] < 0).sum()
            if negative_volume > 0:
                print(f"⚠ volume: Found {negative_volume} negative values")
                self.issues.append("Negative volume values")
                has_negative = True
        
        if not has_negative:
            print("✓ No negative prices or volumes found")
    
    def _check_duplicates(self):
        """Check for duplicate rows."""
        print("\n5. Duplicates Check")
        print("-" * 40)
        
        duplicates = self.df.duplicated().sum()
        
        if duplicates > 0:
            print(f"⚠ Found {duplicates} duplicate rows")
            self.issues.append("Duplicate rows present")
        else:
            print("✓ No duplicate rows found")
    
    def _check_data_range(self):
        """Check data range and provide statistics."""
        print("\n6. Data Range Statistics")
        print("-" * 40)
        
        if isinstance(self.df.index, pd.DatetimeIndex):
            print(f"Date Range: {self.df.index.min().date()} to {self.df.index.max().date()}")
            print(f"Total Records: {len(self.df)}")
            print(f"Date Span: {(self.df.index.max() - self.df.index.min()).days} days")
        
        if 'close' in self.df.columns:
            print(f"Price Range: ${self.df['close'].min():.2f} - ${self.df['close'].max():.2f}")
            print(f"Average Price: ${self.df['close'].mean():.2f}")
            print(f"Current Price: ${self.df['close'].iloc[-1]:.2f}")
        
        if 'volume' in self.df.columns:
            print(f"Average Volume: {self.df['volume'].mean():,.0f}")
    
    def _generate_summary(self) -> Dict[str, Any]:
        """Generate validation summary."""
        print("\n" + "=" * 60)
        print("Validation Summary")
        print("=" * 60)
        
        valid = len(self.issues) == 0
        
        if valid:
            print("\n✓ Data validation PASSED")
            print("  No critical issues found")
        else:
            print(f"\n✗ Data validation FAILED")
            print(f"  Found {len(self.issues)} critical issue(s):")
            for issue in self.issues:
                print(f"  - {issue}")
        
        if self.warnings:
            print(f"\n⚠ {len(self.warnings)} warning(s):")
            for warning in self.warnings:
                print(f"  - {warning}")
        
        print()
        
        return {
            "valid": valid,
            "issues": self.issues,
            "warnings": self.warnings,
            "total_records": len(self.df),
            "date_range": (
                self.df.index.min().date(),
                self.df.index.max().date()
            ) if isinstance(self.df.index, pd.DatetimeIndex) else None
        }


def validate_openbb_output(output) -> Dict[str, Any]:
    """
    Validate OpenBB output object.
    
    Args:
        output: OpenBB output object
        
    Returns:
        Validation results dictionary
    """
    try:
        df = output.to_dataframe()
        validator = DataValidator(df)
        return validator.validate_all()
    except Exception as e:
        print(f"✗ Error converting output to DataFrame: {e}")
        return {
            "valid": False,
            "issues": [f"Conversion error: {e}"],
            "warnings": []
        }


def validate_dataframe(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Validate a pandas DataFrame.
    
    Args:
        df: Pandas DataFrame
        
    Returns:
        Validation results dictionary
    """
    validator = DataValidator(df)
    return validator.validate_all()


# Example usage
if __name__ == "__main__":
    # Example: Validate data from OpenBB
    print("Example Usage:")
    print("-" * 60)
    print("\nWith OpenBB output:")
    print("  from openbb import obb")
    print("  output = obb.equity.price.historical('AAPL')")
    print("  results = validate_openbb_output(output)")
    print("\nWith DataFrame:")
    print("  df = output.to_dataframe()")
    print("  results = validate_dataframe(df)")
    print("\n" + "=" * 60)