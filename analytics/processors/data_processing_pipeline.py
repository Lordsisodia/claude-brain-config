#!/usr/bin/env python3
"""
Advanced Data Processing Pipeline
Designed to trigger agent delegation and complex tool usage for observability testing.
"""

import csv
import json
import logging
import statistics
import datetime
from collections import defaultdict, Counter
from typing import Dict, List, Any, Optional
from pathlib import Path
import sys


class DataValidator:
    """Validates CSV data integrity and structure."""
    
    def __init__(self):
        self.errors = []
        self.warnings = []
    
    def validate_row(self, row: Dict[str, str], row_number: int) -> bool:
        """Validate individual row data."""
        is_valid = True
        
        # Check required fields
        required_fields = ['date', 'product_id', 'sales_amount', 'quantity']
        for field in required_fields:
            if not row.get(field):
                self.errors.append(f"Row {row_number}: Missing required field '{field}'")
                is_valid = False
        
        # Validate data types and formats
        try:
            if row.get('date'):
                datetime.datetime.strptime(row['date'], '%Y-%m-%d')
        except ValueError:
            self.errors.append(f"Row {row_number}: Invalid date format in '{row.get('date')}'")
            is_valid = False
        
        try:
            if row.get('sales_amount'):
                float(row['sales_amount'])
        except ValueError:
            self.errors.append(f"Row {row_number}: Invalid sales_amount '{row.get('sales_amount')}'")
            is_valid = False
        
        try:
            if row.get('quantity'):
                int(row['quantity'])
        except ValueError:
            self.errors.append(f"Row {row_number}: Invalid quantity '{row.get('quantity')}'")
            is_valid = False
        
        return is_valid


class SalesAnalyzer:
    """Performs complex sales data analysis."""
    
    def __init__(self):
        self.data = []
        self.analysis_results = {}
    
    def load_and_validate_data(self, csv_file: str) -> bool:
        """Load CSV data with validation."""
        validator = DataValidator()
        
        try:
            with open(csv_file, 'r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                
                for row_number, row in enumerate(reader, start=2):  # Start at 2 for header row
                    if validator.validate_row(row, row_number):
                        # Convert numeric fields
                        row['sales_amount'] = float(row['sales_amount'])
                        row['quantity'] = int(row['quantity'])
                        row['date'] = datetime.datetime.strptime(row['date'], '%Y-%m-%d')
                        self.data.append(row)
                
                if validator.errors:
                    logging.error(f"Validation errors found: {validator.errors}")
                    return False
                
                if validator.warnings:
                    logging.warning(f"Validation warnings: {validator.warnings}")
                
                logging.info(f"Successfully loaded {len(self.data)} records")
                return True
                
        except FileNotFoundError:
            logging.error(f"CSV file not found: {csv_file}")
            return False
        except Exception as e:
            logging.error(f"Error loading CSV file: {str(e)}")
            return False
    
    def calculate_sales_metrics(self) -> Dict[str, Any]:
        """Calculate comprehensive sales metrics."""
        if not self.data:
            return {}
        
        sales_amounts = [row['sales_amount'] for row in self.data]
        quantities = [row['quantity'] for row in self.data]
        
        metrics = {
            'total_sales': sum(sales_amounts),
            'total_quantity': sum(quantities),
            'average_sale': statistics.mean(sales_amounts),
            'median_sale': statistics.median(sales_amounts),
            'sales_std_dev': statistics.stdev(sales_amounts) if len(sales_amounts) > 1 else 0,
            'min_sale': min(sales_amounts),
            'max_sale': max(sales_amounts),
            'total_transactions': len(self.data)
        }
        
        return metrics
    
    def analyze_by_category(self) -> Dict[str, Dict[str, Any]]:
        """Analyze sales by product category."""
        category_data = defaultdict(list)
        
        for row in self.data:
            category = row.get('category', 'Unknown')
            category_data[category].append(row)
        
        category_analysis = {}
        for category, records in category_data.items():
            sales = [r['sales_amount'] for r in records]
            quantities = [r['quantity'] for r in records]
            
            category_analysis[category] = {
                'total_sales': sum(sales),
                'total_quantity': sum(quantities),
                'transaction_count': len(records),
                'average_sale': statistics.mean(sales),
                'top_products': self._get_top_products_in_category(records)
            }
        
        return category_analysis
    
    def analyze_by_region(self) -> Dict[str, Dict[str, Any]]:
        """Analyze sales by geographical region."""
        region_data = defaultdict(list)
        
        for row in self.data:
            region = row.get('region', 'Unknown')
            region_data[region].append(row)
        
        region_analysis = {}
        for region, records in region_data.items():
            sales = [r['sales_amount'] for r in records]
            
            region_analysis[region] = {
                'total_sales': sum(sales),
                'transaction_count': len(records),
                'average_sale': statistics.mean(sales),
                'top_sales_rep': self._get_top_sales_rep_in_region(records)
            }
        
        return region_analysis
    
    def analyze_sales_trends(self) -> Dict[str, Any]:
        """Analyze sales trends over time."""
        daily_sales = defaultdict(float)
        daily_quantities = defaultdict(int)
        
        for row in self.data:
            date_str = row['date'].strftime('%Y-%m-%d')
            daily_sales[date_str] += row['sales_amount']
            daily_quantities[date_str] += row['quantity']
        
        sorted_dates = sorted(daily_sales.keys())
        
        return {
            'daily_sales': dict(daily_sales),
            'daily_quantities': dict(daily_quantities),
            'date_range': {
                'start': sorted_dates[0] if sorted_dates else None,
                'end': sorted_dates[-1] if sorted_dates else None
            },
            'peak_sales_date': max(daily_sales, key=daily_sales.get) if daily_sales else None,
            'average_daily_sales': statistics.mean(daily_sales.values()) if daily_sales else 0
        }
    
    def _get_top_products_in_category(self, records: List[Dict]) -> List[Dict[str, Any]]:
        """Get top-selling products in a category."""
        product_sales = defaultdict(float)
        product_info = {}
        
        for record in records:
            product_id = record['product_id']
            product_sales[product_id] += record['sales_amount']
            product_info[product_id] = {
                'name': record.get('product_name', 'Unknown'),
                'category': record.get('category', 'Unknown')
            }
        
        top_products = sorted(product_sales.items(), key=lambda x: x[1], reverse=True)[:3]
        
        return [
            {
                'product_id': product_id,
                'name': product_info[product_id]['name'],
                'total_sales': sales
            }
            for product_id, sales in top_products
        ]
    
    def _get_top_sales_rep_in_region(self, records: List[Dict]) -> Dict[str, Any]:
        """Get top sales representative in a region."""
        rep_sales = defaultdict(float)
        
        for record in records:
            rep_name = record.get('sales_rep', 'Unknown')
            rep_sales[rep_name] += record['sales_amount']
        
        if not rep_sales:
            return {'name': 'Unknown', 'total_sales': 0}
        
        top_rep = max(rep_sales.items(), key=lambda x: x[1])
        return {'name': top_rep[0], 'total_sales': top_rep[1]}
    
    def generate_comprehensive_analysis(self) -> Dict[str, Any]:
        """Generate comprehensive analysis results."""
        self.analysis_results = {
            'metadata': {
                'analysis_timestamp': datetime.datetime.now().isoformat(),
                'total_records_processed': len(self.data),
                'analysis_version': '1.0'
            },
            'sales_metrics': self.calculate_sales_metrics(),
            'category_analysis': self.analyze_by_category(),
            'regional_analysis': self.analyze_by_region(),
            'trends_analysis': self.analyze_sales_trends()
        }
        
        return self.analysis_results


class ReportGenerator:
    """Generates formatted reports and outputs."""
    
    def __init__(self):
        self.performance_metrics = {}
    
    def generate_json_report(self, analysis_results: Dict[str, Any], output_file: str) -> bool:
        """Generate JSON report with analysis results."""
        try:
            # Add performance metrics
            analysis_results['performance_metrics'] = self.performance_metrics
            
            with open(output_file, 'w', encoding='utf-8') as file:
                json.dump(analysis_results, file, indent=2, default=str)
            
            logging.info(f"JSON report generated successfully: {output_file}")
            return True
            
        except Exception as e:
            logging.error(f"Error generating JSON report: {str(e)}")
            return False
    
    def generate_summary_report(self, analysis_results: Dict[str, Any]) -> str:
        """Generate human-readable summary report."""
        if not analysis_results:
            return "No analysis results available"
        
        metrics = analysis_results.get('sales_metrics', {})
        categories = analysis_results.get('category_analysis', {})
        regions = analysis_results.get('regional_analysis', {})
        trends = analysis_results.get('trends_analysis', {})
        
        summary = f"""
SALES ANALYSIS SUMMARY REPORT
============================
Generated: {analysis_results.get('metadata', {}).get('analysis_timestamp', 'Unknown')}

OVERALL METRICS:
- Total Sales: ${metrics.get('total_sales', 0):.2f}
- Total Transactions: {metrics.get('total_transactions', 0)}
- Average Sale: ${metrics.get('average_sale', 0):.2f}
- Sales Range: ${metrics.get('min_sale', 0):.2f} - ${metrics.get('max_sale', 0):.2f}

TOP PERFORMING CATEGORIES:
"""
        
        # Add category performance
        sorted_categories = sorted(categories.items(), key=lambda x: x[1]['total_sales'], reverse=True)
        for category, data in sorted_categories[:3]:
            summary += f"- {category}: ${data['total_sales']:.2f} ({data['transaction_count']} transactions)\n"
        
        summary += "\nREGIONAL PERFORMANCE:\n"
        sorted_regions = sorted(regions.items(), key=lambda x: x[1]['total_sales'], reverse=True)
        for region, data in sorted_regions:
            summary += f"- {region}: ${data['total_sales']:.2f} (Avg: ${data['average_sale']:.2f})\n"
        
        if trends.get('date_range'):
            summary += f"\nDATE RANGE: {trends['date_range']['start']} to {trends['date_range']['end']}\n"
            summary += f"PEAK SALES DATE: {trends.get('peak_sales_date', 'Unknown')}\n"
        
        return summary
    
    def track_performance(self, operation: str, duration: float, success: bool):
        """Track performance metrics for operations."""
        if 'operations' not in self.performance_metrics:
            self.performance_metrics['operations'] = []
        
        self.performance_metrics['operations'].append({
            'operation': operation,
            'duration_seconds': duration,
            'success': success,
            'timestamp': datetime.datetime.now().isoformat()
        })


def setup_logging():
    """Setup comprehensive logging configuration."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('/Users/shaansisodia/DEV/data_pipeline.log'),
            logging.StreamHandler(sys.stdout)
        ]
    )


def main():
    """Main execution pipeline."""
    setup_logging()
    logger = logging.getLogger(__name__)
    
    # Initialize components
    analyzer = SalesAnalyzer()
    report_generator = ReportGenerator()
    
    # File paths
    csv_file = '/Users/shaansisodia/DEV/sample_sales_data.csv'
    json_output = '/Users/shaansisodia/DEV/sales_analysis_results.json'
    
    start_time = datetime.datetime.now()
    logger.info("Starting advanced data processing pipeline...")
    
    try:
        # Step 1: Load and validate data
        step_start = datetime.datetime.now()
        success = analyzer.load_and_validate_data(csv_file)
        step_duration = (datetime.datetime.now() - step_start).total_seconds()
        report_generator.track_performance('data_loading', step_duration, success)
        
        if not success:
            logger.error("Data loading failed. Terminating pipeline.")
            return False
        
        # Step 2: Generate comprehensive analysis
        step_start = datetime.datetime.now()
        analysis_results = analyzer.generate_comprehensive_analysis()
        step_duration = (datetime.datetime.now() - step_start).total_seconds()
        report_generator.track_performance('data_analysis', step_duration, True)
        
        # Step 3: Generate reports
        step_start = datetime.datetime.now()
        success = report_generator.generate_json_report(analysis_results, json_output)
        step_duration = (datetime.datetime.now() - step_start).total_seconds()
        report_generator.track_performance('report_generation', step_duration, success)
        
        # Step 4: Generate summary
        step_start = datetime.datetime.now()
        summary = report_generator.generate_summary_report(analysis_results)
        step_duration = (datetime.datetime.now() - step_start).total_seconds()
        report_generator.track_performance('summary_generation', step_duration, True)
        
        # Display summary
        print("\n" + "="*50)
        print(summary)
        print("="*50)
        
        # Calculate total processing time
        total_duration = (datetime.datetime.now() - start_time).total_seconds()
        logger.info(f"Pipeline completed successfully in {total_duration:.2f} seconds")
        
        # Log final performance metrics
        logger.info(f"Performance metrics: {report_generator.performance_metrics}")
        
        return True
        
    except Exception as e:
        logger.error(f"Pipeline execution failed: {str(e)}")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)