import decisionEngine
import pandas as pd
import requests
import webbrowser
import PricePredict

base_url = "https://westus.api.cognitive.microsoft.com/luis/v2.0/apps/7cd9f559-2895-4615-a7b0-f5d2b4ab514a?verbose=true&timezoneOffset=0&subscription-key=58958a3babfd46768a45403652c228fc&q="


def chat_terminal_link(user_msg):
    df = pd.read_csv(r'C:\Users\aadmohan\Desktop\Howathon\count_send.csv')
    list_count_send_btn = list(df['Count_send'])
    intent = df['objective'][0]

    if len(list_count_send_btn) == 0:
        count_send_button = 0
    else:
        count_send_button = int(list_count_send_btn[0])

    '''Introduction'''
    if count_send_button == 0:
        df.at[0, 'Count_send'] = 1
        df.to_csv(r'C:\Users\aadmohan\Desktop\Howathon\count_send.csv',index= False)
        return "Hello this is MnM!\nI will help you in planning and achieving your investment goals.First, I will need to know a bit from you"

    #Objective
    elif count_send_button == 1:
        df.at[0, 'Count_send'] = 2
        df.to_csv(r'C:\Users\aadmohan\Desktop\Howathon\count_send.csv', index=False)
        return "What is your investment objective - Retirement,Future Expenditure or Wealth Creation through an all weather portfolio?\n"

    elif (count_send_button) == 2:
        intent = get_intent_from_user_msg(user_msg, "intent", "topScoringIntent")
        if intent == "Retirement":
            bot_msg = retirement_option(df, count_send_button, user_msg)
            return bot_msg
        elif intent == "Expenditure":
            bot_msg = expenditure_goal_option(df, count_send_button, user_msg)
            return bot_msg
        elif intent == "all weather portfolio":
            bot_msg = all_weather_portfolio(df, count_send_button, user_msg)
            return bot_msg

    elif (count_send_button) > 2:
        if intent == "Retirement":
            bot_msg = retirement_option(df, count_send_button, user_msg)
            return bot_msg
        elif intent == "Expenditure":
            bot_msg = expenditure_goal_option(df, count_send_button, user_msg)
            return bot_msg
        elif intent == "all weather portfolio":
            bot_msg = all_weather_portfolio(df, count_send_button, user_msg)
            return bot_msg

def all_weather_portfolio(df,count_send_button,user_msg):
    if count_send_button == 2:
        PricePredict.main()
        df.at[0, 'Count_send'] = 3
        intent = get_intent_from_user_msg(user_msg,"intent","topScoringIntent")
        df.at[0, 'objective'] = str(intent)
        df.at[0, 'equity'] = 30
        df.at[0, 'bond'] = 55
        df.at[0, 'gold'] = 7.5
        df.at[0, 'commodity'] = 7.5

        df.to_csv(r'C:\Users\aadmohan\Desktop\Howathon\count_send.csv', index=False)
        return "As part of All weather portfolio you need to be in it for atleast 20 years and your allocations are \n Equity:30 \n bond:55 \n gold:7.5 \n commodity:7.5 \n How much would you like to invest?"

    if count_send_button == 3:
        df.at[0, 'Count_send'] = 4
        amount = get_number_from_user_msg(user_msg)
        df.at[0, 'amount'] = str(amount)
        df.to_csv(r'C:\Users\aadmohan\Desktop\Howathon\count_send.csv', index=False)
        webbrowser.open("http://127.0.0.1:8050/pathname/")
        return "Thank You.Will be contacting you shortly for executing the investment steps"


def expenditure_goal_option(df,count_send_button,user_msg):
    if count_send_button == 2:
        PricePredict.main()
        df.at[0, 'Count_send'] = 3
        intent = get_intent_from_user_msg(user_msg,"intent","topScoringIntent")
        df.at[0, 'objective'] = str(intent)
        df.to_csv(r'C:\Users\aadmohan\Desktop\Howathon\count_send.csv', index=False)
        return "What is the expected amount you expect to spend?"

    elif count_send_button == 3:
        df.at[0, 'Count_send'] = 4
        amount = get_number_from_user_msg(user_msg)
        df.at[0, 'amount'] = str(amount)
        df.to_csv(r'C:\Users\aadmohan\Desktop\Howathon\count_send.csv', index=False)
        return "How many years before you want this money?"

    elif count_send_button == 4:
        df.at[0, 'Count_send'] = 5
        time_horizon = get_number_from_user_msg(user_msg)
        df.at[0, 'time_horizon'] = str(time_horizon)
        df.to_csv(r'C:\Users\aadmohan\Desktop\Howathon\count_send.csv', index=False)
        return "How would you profile yourself as Risk taker - Low Risk,Medium Risk or High Risk?\n"

    elif count_send_button == 5:
        df.at[0, 'Count_send'] = 6
        df.at[0, 'risk_profile'] = get_degree_of_risk_from_user_msg(user_msg)
        df.to_csv(r'C:\Users\aadmohan\Desktop\Howathon\count_send.csv', index=False)
        return "Which mode would you like to invest - at one go (Lump Sum) or monthly installments (SIP)"

    elif count_send_button == 6:
        df.at[0, 'Count_send'] = 7
        df.at[0, 'payment_mode'] = get_payment_mode_from_user_msg(user_msg)
        df.to_csv(r'C:\Users\aadmohan\Desktop\Howathon\count_send.csv', index=False)

        future_value = int(df['amount'][0])
        time = int(df['time_horizon'][0])
        payment_mode = str(df['payment_mode'][0])
        rate = select_rate_as_per_time_horizon(time)

        present_value = get_present_value(payment_mode,time,future_value,rate)
        str_every_month = ""
        if payment_mode == "SIP":
            str_every_month = " every month "

        webbrowser.open("http://127.0.0.1:8050/pathname/")
        return "Assuming " + str(rate*100)+"% rate of return on the investment, you need to invest $"+ str(int(present_value)) + str_every_month + " to get $" + str(future_value) + " in " + str(time) + " years."



def retirement_option(df,count_send_button,user_msg):
    if count_send_button == 2:
        df.at[0, 'Count_send'] = 3
        intent = get_intent_from_user_msg(user_msg,"intent","topScoringIntent")
        df.at[0, 'objective'] = str(intent)
        df.to_csv(r'C:\Users\aadmohan\Desktop\Howathon\count_send.csv', index=False)
        return "What is your age?"


    #age
    if count_send_button == 3:
        df.at[0, 'Count_send'] = 4
        age = get_number_from_user_msg(user_msg)

        df.at[0, 'age'] = int(age)
        df.to_csv(r'C:\Users\aadmohan\Desktop\Howathon\count_send.csv', index=False)
        return "How would you profile yourself as Risk taker - Low Risk,Medium Risk or High Risk?\n"

    #Risk
    elif count_send_button == 4:
        df.at[0, 'Count_send'] = 5
        df.at[0, 'risk_profile'] = get_degree_of_risk_from_user_msg(user_msg)
        df.to_csv(r'C:\Users\aadmohan\Desktop\Howathon\count_send.csv', index=False)
        return "What is your monthy income and saving? Please tell the Income first"

    #income
    elif count_send_button == 5:
        df.at[0, 'Count_send'] = 6
        df.at[0, 'income'] = get_income_from_user_msg(user_msg)
        df.to_csv(r'C:\Users\aadmohan\Desktop\Howathon\count_send.csv', index=False)
        return "Now your savings?"

    #saving
    elif count_send_button == 6:
        df.at[0, 'Count_send'] = 7
        df.at[0, 'saving'] = get_income_from_user_msg(user_msg)
        df.to_csv(r'C:\Users\aadmohan\Desktop\Howathon\count_send.csv', index=False)
        return "Do you have an emergency corpus?"

    #emergency corpus
    elif count_send_button == 7:
        df.at[0, 'Count_send'] = 8
        df.at[0, 'is_Emergency_corpus'] = get_status_from_user_msg(user_msg)
        df.to_csv(r'C:\Users\aadmohan\Desktop\Howathon\count_send.csv', index=False)

        user_input_age = int(df['age'][0])
        user_input_risk = str(df['risk_profile'][0])
        user_input_income = int(df['income'][0])
        user_input_saving = int(df['saving'][0])
        user_input_EmergencyCorpus = bool(df['is_Emergency_corpus'][0])


        msg = response_decision_engine(user_input_age,user_input_risk,user_input_saving, user_input_EmergencyCorpus, user_input_income)
        webbrowser.open("http://127.0.0.1:8050/pathname/")
        #resp_msg= get_resp_decision_engine(user_input_age,user_input_risk,user_input_saving, user_input_EmergencyCorpus, user_input_income)
        return msg
def response_decision_engine(user_input_age,user_input_risk,user_input_saving, user_input_EmergencyCorpus, user_input_income):
    resp_msg = requests.get(
        "http://localhost:5000/query-example?user_input_age=" + str(user_input_age) + "&user_input_risk=" + str(user_input_risk) + "&user_input_saving=" + str(user_input_saving) + "&user_input_EmergencyCorpus=" + str(user_input_EmergencyCorpus) + "&user_input_income=" + str(user_input_income))
    dict_resp = resp_msg.json()
    msg = dict_resp['message']
    return msg
    print(msg)


def get_resp_decision_engine(user_input_age,user_input_risk,user_input_saving, user_input_EmergencyCorpus, user_input_income):
    PricePredict.main()
    allocation_bond, allocation_equity = decisionEngine.retirement_asset_allocation(int(user_input_age))
    allocation_bond, allocation_equity = decisionEngine.adjust_asset_allocation_as_per_risk_profile(allocation_bond,
                                                                                                    allocation_equity,
                                                                                                    user_input_risk)
    df=pd.read_csv(r'C:\Users\aadmohan\Desktop\Howathon\count_send.csv')
    df.at[0, 'equity'] = int(allocation_equity*100)
    df.at[0, 'bond'] = int(allocation_bond*100)
    df.to_csv(r'C:\Users\aadmohan\Desktop\Howathon\count_send.csv', index=False)

    SIP_amount = decisionEngine.decide_SIP_amount(user_input_saving, user_input_EmergencyCorpus, user_input_income)
    resp_msg = "Please find your asset allocaion, funds selected and your monthyly SIP.\nAssuming 12% rate of return on your investment, you are expected to receive Rs.50000 per month\n as your Monthly pension after your retirement."
    resp_msg = resp_msg + "\nBond Allocation :" + str(int(allocation_bond*100)) + "\nEquity Allocation :" + str(
        int(allocation_equity*100)) + "\nSIP Amount :" + str(SIP_amount)
    return resp_msg

def get_degree_of_risk_from_user_msg(user_msg):

    url = base_url + user_msg +")"

    r = requests.get(url)

    dict_request = dict(r.json())
    dict_entities = dict_request['entities'][0]
    dict_resolution = dict_entities['resolution']
    risk_value = dict_resolution['values'][0]
    return risk_value




def get_intent_from_user_msg(user_msg,dict_key,dict_key2):
    base_url = "https://westus.api.cognitive.microsoft.com/luis/v2.0/apps/7cd9f559-2895-4615-a7b0-f5d2b4ab514a?verbose=true&timezoneOffset=0&subscription-key=58958a3babfd46768a45403652c228fc&q="
    url = base_url + user_msg +")"

    r = requests.get(url)

    dict_request = dict(r.json())
    dict_intent = dict_request[dict_key2]

    intent = dict_intent[dict_key]
    return intent

def get_number_from_user_msg(user_msg):
    base_url = "https://westus.api.cognitive.microsoft.com/luis/v2.0/apps/7cd9f559-2895-4615-a7b0-f5d2b4ab514a?verbose=true&timezoneOffset=0&subscription-key=58958a3babfd46768a45403652c228fc&q="
    url = base_url + user_msg +")"

    r = requests.get(url)

    dict_request = dict(r.json())
    dict_entities = dict_request['entities'][0]
    age = dict_entities['entity']

    return age

def get_income_from_user_msg(user_msg):
    url = base_url + user_msg +")"

    r = requests.get(url)

    dict_request = dict(r.json())
    dict_entities = dict_request['entities'][0]
    age = dict_entities['entity']

    return age
def get_payment_mode_from_user_msg(user_msg):
    url = base_url + user_msg +")"

    r = requests.get(url)

    dict_request = dict(r.json())
    dict_entities = dict_request['entities'][0]
    status = dict_entities['type']
    return status

def get_status_from_user_msg(user_msg):
    url = base_url + user_msg +")"
    try:
        r = requests.get(url)
    except:
        r = requests.get(url)


    dict_request = dict(r.json())
    dict_entities = dict_request['entities'][0]
    status = dict_entities['type']
    if "affirmative" == status:
        return True
    return False

def get_present_value(payment_mode,time,future_value,rate):

    if payment_mode == "LumpSum":
        present_value = calculate_pv(future_value,time,rate)
    elif payment_mode == "SIP":
        present_value = sip_calculator(future_value, time, rate)
    return present_value

def sip_calculator(Future_value,time,rate):

    amount = (Future_value * (rate))/((1 + rate)**(time) - 1)
    amount = amount / 12
    return amount



def calculate_pv(future_value,time,rate):

    present_value = (future_value / ((1 + rate)**time))
    return present_value
def select_rate_as_per_time_horizon(time):
    df = pd.read_csv(r'C:\Users\aadmohan\Desktop\Howathon\count_send.csv')
    df.at[0, 'equity'] = 0
    df.at[0, 'bond'] = 100
    risk_profile =df['risk_profile'][0]

    if time <6:
        rate = 0.06
        df.at[0, 'equity'] = 0
        df.at[0, 'bond'] = 100
    elif ((time > 5) and (time <11)) or (risk_profile=="Low")  :

        df.at[0, 'equity'] = 20
        df.at[0, 'bond'] = 80
        rate = 0.09
    elif time >10:
        df.at[0, 'equity'] = 40
        df.at[0, 'bond'] = 60
        rate = 0.12
    df.to_csv(r'C:\Users\aadmohan\Desktop\Howathon\count_send.csv', index=False)
    return rate



if __name__ == '__main__':
    df= pd.read_csv(r'C:\Users\aadmohan\Desktop\Howathon\count_send.csv')
    print(get_present_value(df))
    #resp_msg = get_resp_decision_engine(50,"high risk",20000,True,50000)
    #print(resp_msg)



