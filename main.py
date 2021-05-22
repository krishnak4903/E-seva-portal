from flask import Flask, request, redirect
from flask import render_template
import requests
from twilio.rest import Client
import requests_cache
account_sid = 'AC5477b5fadc57c1fc8de386ceeb593b88'
auth_token = '7f271b635df00e2ecf0a4cf6759f930d'
client = Client(account_sid, auth_token)
app = Flask(__name__)

@app.route('/')
def registration_form():
    return render_template('login_page.html')


@app.route('/login_page', methods=['POST', 'GET'])
def login_page():
    if request.method == "POST":
        user_name = request.form.get('username')
        email_id = request.form.get('email_id')
        aadhar_card = request.form.get('aadhar_card')
        travelling_from = request.form.get('Travelling_from')
        source_district=request.form.get('source_district')
        destination = request.form.get('Destination')
        dest_district = request.form.get('dest_district')
        phone_no = request.form.get('phoneno')
        date_of_travel = request.form.get('date_of_travel')
        r = requests.get('https://api.covid19india.org/v4/data.json')
        json_data=r.json()
        cnt = json_data[destination]['districts'][dest_district]['total']['confirmed']
        pop = json_data[destination]['districts'][dest_district]['meta']['population']
        travel_pass = ((cnt / pop) * 100)
        status = 'Not confirmed'
        if travel_pass < 30 and request.method == "POST":
            status = 'confirmed'
            client.messages.create(to=f'{phone_no}',
                                   from_="+13345696145",
                                   body="Hello" + " " + user_name + " " + "Your Travel From" + " " + source_district
                                        + " " + "To" + " " + dest_district + " " + "Has" + " " + status + "on " +
                                         " "+date_of_travel)
            return render_template('user_registration.html', var=user_name, var1=email_id, var2=aadhar_card,
                                   var3=travelling_from, var4=source_district, var5=destination,
                                   var6=dest_district, var7=phone_no, var8=date_of_travel, var9=status)
        else:
            status = 'Not confirmed'
            client.messages.create(to=f'{phone_no}',
                                   from_="+13345696145",
                                   body="Hello" + " " + user_name + " " + "Your Travel From" + " " + source_district
                                        + " " + "To" + " " + dest_district + " " + "Has" + " " + status + "on" +
                                        " " + date_of_travel + " " + "Apply later")
            return render_template('user_registration.html', var=user_name, var1=email_id, var2=aadhar_card,
                                   var3=travelling_from, var4=source_district, var5=destination,
                                   var6=dest_district, var7=phone_no, var8=date_of_travel, var9=status)


if __name__ == '__main__':
    app.run()