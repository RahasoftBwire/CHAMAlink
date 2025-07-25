from flask import Blueprint, render_template, request, jsonify, make_response, send_file, flash, redirect, url_for, current_app
from flask_login import login_required, current_user
from app import db
from app.models import Chama, Transaction, LoanApplication, Penalty, MpesaTransaction, User, chama_members
from app.utils.permissions import chama_member_required, chama_admin_required
from datetime import datetime, timedelta
from sqlalchemy import func, and_, or_
import io
import base64

# Optional analytics imports - gracefully handle if not installed
try:
    import pandas as pd
    PANDAS_AVAILABLE = True
except ImportError:
    PANDAS_AVAILABLE = False

try:
    import matplotlib
    matplotlib.use('Agg')  # Use non-interactive backend
    import matplotlib.pyplot as plt
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False

try:
    import seaborn as sns
    SEABORN_AVAILABLE = True
except ImportError:
    SEABORN_AVAILABLE = False

try:
    from reportlab.lib.pagesizes import letter, A4
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.lib.colors import black, grey, blue, green, red
    from reportlab.lib import colors
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False

reports_bp = Blueprint('reports', __name__, url_prefix='/reports')

@reports_bp.route('/chama/<int:chama_id>')
@login_required
@chama_member_required
def chama_dashboard(chama_id):
    """Financial reports dashboard for chama"""
    chama = Chama.query.get_or_404(chama_id)
    
    # Get date range from query parameters
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    # Default to last 30 days
    if not start_date:
        start_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
    if not end_date:
        end_date = datetime.now().strftime('%Y-%m-%d')
    
    # Convert to datetime objects
    start_dt = datetime.strptime(start_date, '%Y-%m-%d')
    end_dt = datetime.strptime(end_date, '%Y-%m-%d') + timedelta(days=1)
    
    # Get transactions in date range
    transactions = Transaction.query.filter(
        Transaction.chama_id == chama_id,
        Transaction.created_at >= start_dt,
        Transaction.created_at < end_dt
    ).order_by(Transaction.created_at.desc()).all()
    
    # Get loans in date range
    loans = LoanApplication.query.filter(
        LoanApplication.chama_id == chama_id,
        LoanApplication.created_at >= start_dt,
        LoanApplication.created_at < end_dt
    ).all()
    
    # Get penalties in date range
    penalties = Penalty.query.filter(
        Penalty.chama_id == chama_id,
        Penalty.created_at >= start_dt,
        Penalty.created_at < end_dt
    ).all()
    
    # Calculate summary statistics
    total_contributions = sum(t.amount for t in transactions if t.type == 'contribution')
    total_loans = sum(l.amount for l in loans if l.status == 'approved')
    total_penalties = sum(p.amount for p in penalties)
    total_loan_repayments = sum(t.amount for t in transactions if t.type == 'loan_repayment')
    
    # Get member statistics
    member_contributions = {}
    for transaction in transactions:
        if transaction.type == 'contribution':
            if transaction.user_id not in member_contributions:
                member_contributions[transaction.user_id] = 0
            member_contributions[transaction.user_id] += transaction.amount
    
    # Get top contributors
    top_contributors = []
    for user_id, amount in sorted(member_contributions.items(), key=lambda x: x[1], reverse=True)[:5]:
        user = User.query.get(user_id)
        if user:
            top_contributors.append({'user': user, 'amount': amount})
    
    user_role = get_user_chama_role(current_user.id, chama_id)
    
    return render_template('reports/dashboard.html',
                         chama=chama,
                         transactions=transactions,
                         loans=loans,
                         penalties=penalties,
                         total_contributions=total_contributions,
                         total_loans=total_loans,
                         total_penalties=total_penalties,
                         total_loan_repayments=total_loan_repayments,
                         top_contributors=top_contributors,
                         start_date=start_date,
                         end_date=end_date,
                         user_role=user_role)

@reports_bp.route('/chama/<int:chama_id>/export/<format>')
@login_required
@chama_member_required
def export_report(chama_id, format):
    """Export chama financial report"""
    chama = Chama.query.get_or_404(chama_id)
    
    # Get date range from query parameters
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    # Default to last 30 days
    if not start_date:
        start_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
    if not end_date:
        end_date = datetime.now().strftime('%Y-%m-%d')
    
    # Convert to datetime objects
    start_dt = datetime.strptime(start_date, '%Y-%m-%d')
    end_dt = datetime.strptime(end_date, '%Y-%m-%d') + timedelta(days=1)
    
    if format == 'csv':
        return export_csv(chama, start_dt, end_dt)
    elif format == 'pdf':
        return export_pdf(chama, start_dt, end_dt)
    else:
        return jsonify({'error': 'Invalid format'}), 400

def export_csv(chama, start_dt, end_dt):
    """Export financial data as CSV"""
    # Get transactions
    transactions = Transaction.query.filter(
        Transaction.chama_id == chama.id,
        Transaction.created_at >= start_dt,
        Transaction.created_at < end_dt
    ).all()
    
    # Create CSV content manually
    output = io.StringIO()
    
    # Write header
    output.write('Date,Type,Amount,Description,User,Status\n')
    
    # Write data rows
    for transaction in transactions:
        date = transaction.created_at.strftime('%Y-%m-%d %H:%M:%S')
        trans_type = transaction.type.replace('_', ' ').title()
        amount = str(transaction.amount)
        description = transaction.description.replace(',', ';') if transaction.description else ''
        user = transaction.user.username if transaction.user else 'System'
        status = transaction.status
        
        output.write(f'"{date}","{trans_type}",{amount},"{description}","{user}","{status}"\n')
    
    output.seek(0)
    
    response = make_response(output.getvalue())
    response.headers['Content-Type'] = 'text/csv'
    response.headers['Content-Disposition'] = f'attachment; filename="{chama.name}_financial_report_{start_dt.strftime("%Y%m%d")}_to_{end_dt.strftime("%Y%m%d")}.csv"'
    
    return response

def export_pdf(chama, start_dt, end_dt):
    """Export financial report as PDF"""
    
    if not REPORTLAB_AVAILABLE:
        # Return an error response if reportlab is not available
        return jsonify({
            'error': 'PDF export not available. Please install analytics packages.',
            'install_command': 'pip install -r requirements-analytics.txt'
        }), 503
    
    # Create PDF buffer
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    
    # Styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        textColor=blue,
        alignment=1  # Center alignment
    )
    
    # Content
    content = []
    
    # Title
    title = Paragraph(f"Financial Report - {chama.name}", title_style)
    content.append(title)
    content.append(Spacer(1, 12))
    
    # Date range
    date_range = Paragraph(f"Report Period: {start_dt.strftime('%Y-%m-%d')} to {end_dt.strftime('%Y-%m-%d')}", styles['Normal'])
    content.append(date_range)
    content.append(Spacer(1, 12))
    
    # Summary statistics
    transactions = Transaction.query.filter(
        Transaction.chama_id == chama.id,
        Transaction.created_at >= start_dt,
        Transaction.created_at < end_dt
    ).all()
    
    loans = LoanApplication.query.filter(
        LoanApplication.chama_id == chama.id,
        LoanApplication.created_at >= start_dt,
        LoanApplication.created_at < end_dt
    ).all()
    
    penalties = Penalty.query.filter(
        Penalty.chama_id == chama.id,
        Penalty.created_at >= start_dt,
        Penalty.created_at < end_dt
    ).all()
    
    total_contributions = sum(t.amount for t in transactions if t.type == 'contribution')
    total_loans = sum(l.amount for l in loans if l.status == 'approved')
    total_penalties = sum(p.amount for p in penalties)
    
    # Summary table
    summary_data = [
        ['Metric', 'Amount (KES)'],
        ['Total Contributions', f'{total_contributions:,.0f}'],
        ['Total Loans Disbursed', f'{total_loans:,.0f}'],
        ['Total Penalties', f'{total_penalties:,.0f}'],
        ['Current Balance', f'{chama.total_balance:,.0f}'],
    ]
    
    summary_table = Table(summary_data, colWidths=[3*inch, 2*inch])
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    content.append(Paragraph("Financial Summary", styles['Heading2']))
    content.append(summary_table)
    content.append(Spacer(1, 24))
    
    # Transactions table
    if transactions:
        trans_data = [['Date', 'Type', 'Amount', 'User', 'Description']]
        for transaction in transactions[:20]:  # Limit to first 20 transactions
            trans_data.append([
                transaction.created_at.strftime('%Y-%m-%d'),
                transaction.type.replace('_', ' ').title(),
                f'{transaction.amount:,.0f}',
                transaction.user.username if transaction.user else 'System',
                transaction.description[:30] + '...' if len(transaction.description) > 30 else transaction.description
            ])
        
        trans_table = Table(trans_data, colWidths=[1.2*inch, 1.3*inch, 1*inch, 1*inch, 1.5*inch])
        trans_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTSIZE', (0, 1), (-1, -1), 8)
        ]))
        
        content.append(Paragraph("Recent Transactions", styles['Heading2']))
        content.append(trans_table)
    
    # Build PDF
    doc.build(content)
    
    # Return PDF file
    buffer.seek(0)
    return send_file(
        io.BytesIO(buffer.read()),
        mimetype='application/pdf',
        as_attachment=True,
        download_name=f'{chama.name}_financial_report_{start_dt.strftime("%Y%m%d")}_to_{end_dt.strftime("%Y%m%d")}.pdf'
    )

@reports_bp.route('/chama/<int:chama_id>/chart/<chart_type>')
@login_required
@chama_member_required
def generate_chart(chama_id, chart_type):
    """Generate charts for financial data"""
    
    if not MATPLOTLIB_AVAILABLE or not SEABORN_AVAILABLE:
        # Return an error response if matplotlib/seaborn is not available
        return jsonify({
            'error': 'Chart generation not available. Please install analytics packages.',
            'install_command': 'pip install -r requirements-analytics.txt'
        }), 503
    
    chama = Chama.query.get_or_404(chama_id)
    
    # Get date range
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    if not start_date:
        start_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
    if not end_date:
        end_date = datetime.now().strftime('%Y-%m-%d')
    
    start_dt = datetime.strptime(start_date, '%Y-%m-%d')
    end_dt = datetime.strptime(end_date, '%Y-%m-%d') + timedelta(days=1)
    
    # Set up matplotlib
    plt.style.use('seaborn-v0_8')
    fig, ax = plt.subplots(figsize=(10, 6))
    
    if chart_type == 'contributions':
        # Monthly contributions chart
        transactions = Transaction.query.filter(
            Transaction.chama_id == chama_id,
            Transaction.type == 'contribution',
            Transaction.created_at >= start_dt,
            Transaction.created_at < end_dt
        ).all()
        
        # Group by month
        monthly_data = {}
        for transaction in transactions:
            month = transaction.created_at.strftime('%Y-%m')
            if month not in monthly_data:
                monthly_data[month] = 0
            monthly_data[month] += transaction.amount
        
        months = list(monthly_data.keys())
        amounts = list(monthly_data.values())
        
        ax.bar(months, amounts, color='#28a745')
        ax.set_title('Monthly Contributions')
        ax.set_xlabel('Month')
        ax.set_ylabel('Amount (KES)')
        plt.xticks(rotation=45)
        
    elif chart_type == 'member_contributions':
        # Member contributions pie chart
        transactions = Transaction.query.filter(
            Transaction.chama_id == chama_id,
            Transaction.type == 'contribution',
            Transaction.created_at >= start_dt,
            Transaction.created_at < end_dt
        ).all()
        
        member_data = {}
        for transaction in transactions:
            username = transaction.user.username if transaction.user else 'Unknown'
            if username not in member_data:
                member_data[username] = 0
            member_data[username] += transaction.amount
        
        if member_data:
            labels = list(member_data.keys())
            sizes = list(member_data.values())
            
            ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
            ax.set_title('Member Contributions Distribution')
        else:
            ax.text(0.5, 0.5, 'No data available', transform=ax.transAxes, ha='center', va='center')
            ax.set_title('Member Contributions Distribution')
    
    elif chart_type == 'balance_trend':
        # Balance trend over time
        transactions = Transaction.query.filter(
            Transaction.chama_id == chama_id,
            Transaction.created_at >= start_dt,
            Transaction.created_at < end_dt
        ).order_by(Transaction.created_at).all()
        
        dates = []
        balances = []
        running_balance = 0
        
        for transaction in transactions:
            dates.append(transaction.created_at.date())
            if transaction.type in ['contribution', 'loan_repayment', 'penalty_payment']:
                running_balance += transaction.amount
            elif transaction.type == 'loan_disbursement':
                running_balance -= transaction.amount
            balances.append(running_balance)
        
        if dates and balances:
            ax.plot(dates, balances, marker='o', color='#007bff')
            ax.set_title('Balance Trend')
            ax.set_xlabel('Date')
            ax.set_ylabel('Balance (KES)')
            plt.xticks(rotation=45)
        else:
            ax.text(0.5, 0.5, 'No data available', transform=ax.transAxes, ha='center', va='center')
            ax.set_title('Balance Trend')
    
    plt.tight_layout()
    
    # Save to buffer
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png', dpi=300, bbox_inches='tight')
    buffer.seek(0)
    
    # Encode as base64
    image_base64 = base64.b64encode(buffer.getvalue()).decode()
    plt.close()
    
    return jsonify({'image': image_base64})

@reports_bp.route('/chama/<int:chama_id>/analytics')
@login_required
@chama_member_required
def chama_analytics(chama_id):
    """Analytics dashboard for specific chama"""
    try:
        chama = Chama.query.get_or_404(chama_id)
        
        # Get chama statistics
        from sqlalchemy import func, extract
        from datetime import datetime, timedelta
        
        # Contribution trends (last 6 months)
        six_months_ago = datetime.now() - timedelta(days=180)
        monthly_contributions = db.session.query(
            extract('year', Transaction.created_at).label('year'),
            extract('month', Transaction.created_at).label('month'),
            func.sum(Transaction.amount).label('total')
        ).filter(
            Transaction.chama_id == chama_id,
            Transaction.type == 'contribution',
            Transaction.created_at >= six_months_ago
        ).group_by(
            extract('year', Transaction.created_at),
            extract('month', Transaction.created_at)
        ).order_by('year', 'month').all()
        
        # Member activity analysis
        member_activity = db.session.query(
            User.username,
            func.count(Transaction.id).label('transaction_count'),
            func.sum(Transaction.amount).label('total_contributed')
        ).join(Transaction).filter(
            Transaction.chama_id == chama_id,
            Transaction.type == 'contribution'
        ).group_by(User.id, User.username).all()
        
        # Recent financial summary
        total_contributions = db.session.query(func.sum(Transaction.amount)).filter(
            Transaction.chama_id == chama_id,
            Transaction.type == 'contribution'
        ).scalar() or 0
        
        total_loans = db.session.query(func.sum(Transaction.amount)).filter(
            Transaction.chama_id == chama_id,
            Transaction.type == 'loan'
        ).scalar() or 0
        
        # Growth metrics
        current_members = len(chama.members)
        last_month = datetime.now() - timedelta(days=30)
        new_members = db.session.query(func.count(chama_members.c.user_id)).filter(
            chama_members.c.chama_id == chama_id,
            chama_members.c.joined_at >= last_month
        ).scalar() or 0
        
        analytics_data = {
            'chama': chama,
            'monthly_contributions': [
                {
                    'month': f"{int(contrib.year)}-{int(contrib.month):02d}",
                    'total': float(contrib.total)
                } for contrib in monthly_contributions
            ],
            'member_activity': [
                {
                    'name': activity.username,
                    'transactions': activity.transaction_count,
                    'total': float(activity.total_contributed)
                } for activity in member_activity
            ],
            'summary': {
                'total_contributions': total_contributions,
                'total_loans': total_loans,
                'current_balance': chama.total_balance,
                'member_count': current_members,
                'new_members_month': new_members
            }
        }
        
        return render_template('reports/analytics.html', 
                             analytics=analytics_data,
                             chama=chama)
    
    except Exception as e:
        current_app.logger.error(f"Analytics error: {e}")
        flash('Error loading analytics. Please try again later.', 'error')
        return redirect(url_for('chama.chama_detail', chama_id=chama_id))

def get_user_chama_role(user_id, chama_id):
    """Get the role of a user in a specific chama"""
    membership = db.session.query(chama_members).filter(
        chama_members.c.user_id == user_id,
        chama_members.c.chama_id == chama_id
    ).first()
    
    return membership.role if membership else None
