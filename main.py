import streamlit as st
import pandas as pd
from botocore.exceptions import ClientError
import boto3


# Load the CSV file into a DataFrame
def load_data():
	data = pd.read_csv('data.csv')
	return data

aws_region = 'us-east-1'
aws_access_key_id = 'AKIAVRUVSR4ABH4IXGW2'
aws_secret_access_key = 'OUPYRhfVLeU9x+MeMP3MTvE75WIwif+ZsOTnEQl0'

def send_html_email(subject, html_body, from_email, to_emails):
	# Create a new SES resource and specify a region (replace 'your-region' with the actual region)
	ses = boto3.client(
		'ses',
		region_name=aws_region,
		aws_access_key_id=aws_access_key_id,
		aws_secret_access_key=aws_secret_access_key
	)

	# Try to send the email.
	try:
		# Provide the contents of the email.
		response = ses.send_email(Destination={'ToAddresses': to_emails, },
		                          Message={'Body': {'Html': {'Charset': 'UTF-8', 'Data': html_body, }, },
		                                   'Subject': {'Charset': 'UTF-8', 'Data': subject, }, }, Source=from_email, )
	except ClientError as e:
		print(e.response['Error']['Message'])
	else:
		print("Email sent! Message ID:"),
		print(response['MessageId'])


# Example usage
subject = "Your HTML Email Subject"
html_body = """
<html>
    <head></head>
    <body>
        <h1>Hello!</h1>
        <p>This is a test HTML email.</p>
    </body>
</html>
"""

html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body {
            background-color: #f5fbfb;
            color: #121620;
            font-family: 'Montserrat', sans-serif;
        }
        h1 {
            font-size: 72px;
            font-weight: bold;
            margin-bottom: 30px;
        }
        ul {
            list-style: none;
            padding: 0;
        }
        li {
            font-size: 24px;
            font-weight: medium;
            margin-bottom: 10px;
        }
    </style>
</head>

"""

html_body = """
<body>
    <h1>Your daily feed</h1>
    <ul>
        {list_items}
    </ul>
</body>
</html>
"""


# Function to render HTML with a list of sentences
def render_html(sentences):
	list_items = '\n'.join(f'<li>{sentence}</li>' for sentence in sentences)
	return html_template + html_body.format(list_items=list_items)


def add_email_to_verified_emails(email):
	ses_client = boto3.client(
		'ses',
		region_name=aws_region,
		aws_access_key_id=aws_access_key_id,
		aws_secret_access_key=aws_secret_access_key
	)
	try:
		ses_client.verify_email_identity(EmailAddress=email)
		return True
	except Exception as e:
		return False
# Main app function
def main():
	st.set_page_config(page_title="Ooluck - Data Explorer", page_icon="favicon.ico", layout='wide',
	                   initial_sidebar_state='auto')


	st.title('Ooluck - Data Explorer')

	data = load_data()

	st.sidebar.header('Search Filters')
	selected_sentiments = st.sidebar.multiselect('Sentiment', options=data['sentiment'].unique(),
	                                             default=data['sentiment'].unique())
	selected_categories = st.sidebar.multiselect('Category', options=data['category'].unique(),
	                                             default=data['category'].unique())
	filtered_data = data[(data['sentiment'].isin(selected_sentiments)) & (data['category'].isin(selected_categories))]

	if not filtered_data.empty:
		st.write(filtered_data)
	else:
		st.write("No results found based on the filters.")

	email_address = st.text_input("Enter your email address")

	if st.button("Send Daily Feed") and email_address:
		# Select random 10 items from the data, adjust this logic to your dataset structure
		selected_items = filtered_data.sample(n=min(10, len(filtered_data))).to_dict('records')  # Convert to list of dicts
		sentences = [f"{item['story']}" for item in selected_items]  # Adjust to your data columns
		html_content = render_html(sentences)
		subject = "Your Daily Feed"
		from_email = "oguzvuruskaner@gmail.com"  # Replace with your actual SES verified email
		to_emails = [email_address]
		send_html_email(subject, html_content, from_email, to_emails)
		st.success("Email sent successfully!")

	if st.button("Register Email"):
		if add_email_to_verified_emails(email_address):
			st.success("Registration email is sent successfully! Please look at your email.")
		else:
			st.error("Error adding email. Please try again.")

if __name__ == '__main__':
	main()
