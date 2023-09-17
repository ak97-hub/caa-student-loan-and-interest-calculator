import streamlit as st 

st.set_page_config(layout="wide")

get_periodic_rate = lambda annual_rate: annual_rate / 12
get_number_of_payments = lambda years: years * 12

def get_monthly_loan_payment(principal, annual_interest, years):
    periodic_rate = get_periodic_rate(annual_interest)
    number_of_payments = get_number_of_payments(years)
    numerator = ((1 + periodic_rate) ** number_of_payments) - 1
    denominator = (periodic_rate * ((1 + periodic_rate) ** number_of_payments))

    return principal / (numerator / denominator)

def get_returns(PV, PMT, rate, years):
    step1 = ((1 + rate) ** years) - 1
    step2 = PMT * (step1 / rate)
    step3 = PV * ((1 + rate) ** years)
    return step2 + step3

def get_annual_payments(monthly_payments_student_loans):
    return 12 * monthly_payments_student_loans


def get_total_interest_paid(annual_payments_student_loans, years, student_loans_total):
    return annual_payments_student_loans * years_to_pay_off_loans - student_loans_total

st.header("Welcome to CAA Chabely Investment Calculator!!")
st.write('''Hey, welcome to my investment calculator! 
            We've created this calculator to make things a bit more understandable and fun for you. 
            Dive in, explore, and hopefully, it'll shed some light on your goals. 
            However, please keep in mind this is not meant to provide any financial advice. 
            It's important to remember that while this tool aims to simplify complex calculations, 
            it is by no means a source of financial advice or guidance. 
            Always consult with a qualified financial expert for any serious financial decisions!! 
            This calculator is for exploration and entertainment, and not to provide financial recommendations''')

st.write('')
st.write('''Also if you found this calculator useful,
            and would love to see more of what I do, please check out my [Youtube channel](https://www.youtube.com/@CAALifestyle) 
            and consider being a subscriber!!! 
         ''')
st.markdown('---')
st.subheader('*Student Loans & Investments Calculator:')
st.markdown('''
Here we have an example below. 
<ul>
    <li>John Doe has a <b>yearly budget of $35,000</b> and 
    he's trying to figure how to split that budget between <b>investing for retirement</b> and <b>student loans</b>.</li>
    <li>His <b>original investment</b> in his retirement is only <b>$10,000</b>. </li>
    <li>And he has <b>$55,000 in student loans with 7% interest</b> --Not good!! </li>
    <li>He ideally wants to <b>pay off his student loans in 10 years</b>! And he wants to <b>retire in 35 years.</b></li>
    <li>Johns spoke to his fininacial advisor who said he expects roughly <b>6% returns.</b>.</li>
    <li>John also heard that inflation will mean his retirement amount could mean less; 
    he thinks there will be a <b>3% inflation rate</b>.</li>
</ul>''', unsafe_allow_html= True)
            
st.write('''\n\nLets begin by inputting these numbers for John below!!''')
st.markdown("---")
st.write('')
left_column, right_column = st.columns(2)

st.markdown(
        """<style>
    div[class*="stSlider"] > label > div[data-testid="stMarkdownContainer"] > p {
        font-size: 17px;
    }
        </style>
        """, unsafe_allow_html=True)

st.markdown(
        """<style>
    div[class*="stNumberInput"] > label > div[data-testid="stMarkdownContainer"] > p {
        font-size: 17px;
    }
        </style>
        """, unsafe_allow_html=True)

with left_column:
    yearly_budget = st.slider("Enter your yearly budget (investments + student loans):", min_value=0, max_value=300_000, step=1_000, value=35_000)
    original_invested = st.number_input("Enter your original investment:", min_value=0, max_value=1_000_000, step=10_000, value=10_000)
    student_loans = st.number_input("Enter your total student loans:", min_value=0, max_value=1_000_000, step=10_000, value=55_000)
    annual_interest_student_loans = st.slider("Enter annual interest on student loans:", min_value=0.5, max_value=25.0, step=0.1, value=7.0)
    annual_returns_interest = st.slider("Expected annual interest returns:", min_value=0.5, max_value=25.0, step=0.1, value=6.0)
    years_to_pay_off_loans = st.number_input("Enter number of years to pay off loans:", min_value=1, max_value=35, step=5, value=10)
    years_to_investment = st.number_input("Enter years before you retire:", min_value=5, max_value=60, step=5, value=35)
    inflation_rate = st.slider('Expected annual inflation rate: ', min_value=0.5, max_value=25.0, step=0.5, value = 3.0)

def inflation_adjusted(future_principal,number_of_years,inflation_rate):
    return future_principal / (1 + inflation_rate) ** number_of_years

annual_interest_student_loans = annual_interest_student_loans / 100
annual_returns_interest = annual_returns_interest / 100
inflation_rate = inflation_rate / 100
inflation_rate_adjusted = ((1 + annual_returns_interest) / (1 + inflation_rate)) - 1

monthly_payments_student_loans = get_monthly_loan_payment(principal=student_loans, 
                                                          years=years_to_pay_off_loans, 
                                                          annual_interest=annual_interest_student_loans)
annual_payments_student_loans = get_annual_payments(monthly_payments_student_loans)
total_interest_paid_sl = get_total_interest_paid(annual_payments_student_loans, 
                                                years=years_to_pay_off_loans, 
                                                student_loans_total=student_loans)
total_annual_returns_before_loans_paid_off = get_returns(PV=original_invested,
                                                        PMT=yearly_budget - annual_payments_student_loans,
                                                        rate=annual_returns_interest,
                                                        years=years_to_pay_off_loans)

total_annual_returns = get_returns(PV=total_annual_returns_before_loans_paid_off,
                                                        PMT=yearly_budget,
                                                        rate=annual_returns_interest,
                                                        years=years_to_investment - years_to_pay_off_loans)

inflation_annual_returns_before_loans_paid_off = get_returns(PV=original_invested,
                                                        PMT=yearly_budget - annual_payments_student_loans,
                                                        rate=inflation_rate_adjusted,
                                                        years=years_to_pay_off_loans)

inflation_adjusted_returns = get_returns(PV=inflation_annual_returns_before_loans_paid_off,
                                                        PMT=yearly_budget,
                                                        rate=inflation_rate_adjusted,
                                                        years=years_to_investment - years_to_pay_off_loans)

monthly_payments_student_loans = '{:,.2f}'.format(round(monthly_payments_student_loans, 2))
annual_payments_student_loans = '{:,.2f}'.format(round(annual_payments_student_loans, 2))
total_annual_returns = '{:,.2f}'.format(round(total_annual_returns, 2))
total_interest_paid_sl = '{:,.2f}'.format(round(total_interest_paid_sl, 2))
inflation_adjusted_returns = '{:,.2f}'.format(round(inflation_adjusted_returns, 2))

with right_column:
    st.markdown(
        f"""
        <div style="background-color: #FF5732; padding: 25px; border-radius: 10px;">
            <h2 style="color: white;">*Results:</h2>
            <h5 style="color: white;">How much is John's student loan monthly payments?</h5>
            <p style="color: white; font-size: 27px;">${monthly_payments_student_loans}</p>
            <h5 style="color: white;">How much is John's student loan annual payments?</h5>
            <p style="color: white; font-size: 27px;">${annual_payments_student_loans}</p>
            <h5 style="color: white;">**How much will John retire with (before taxes)?</h5>
            <p style="color: white; font-size: 27px;">${total_annual_returns}</p>
            <h5 style="color: white;">**How much will John retire with? (inflation adjusted + before taxes)?</h5>
            <p style="color: white; font-size: 27px;">${inflation_adjusted_returns}</p>
            <h5 style="color: white;">How much will John pay in student loan interest?</h5>
            <p style="color: white; font-size: 27px;">${total_interest_paid_sl}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

st.write('')
st.write('')
st.write('')
st.write('''*Disclaimer: This interest calculator is provided for entertainment purposes only. 
            It is not intended to constitute financial advice or serve as a substitute for professional financial guidance. 
            The results generated by this calculator should not be considered as recommendations or endorsements for any financial decisions. 
            Always consult with a qualified financial advisor or expert before making any financial choices or investments. 
            Your personal financial situation may vary, and this calculator is not tailored to your specific needs or circumstances.''')

st.write('**This retirement value is not reflective of fees, taxes, nor investment vehicles.')