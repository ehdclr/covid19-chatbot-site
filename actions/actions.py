# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher


import json
import requests
import xmltodict
from datetime import date, timedelta



def get_corona_data(startCreateDt, endCreateDt):
    url = 'http://openapi.data.go.kr/openapi/service/rest/Covid19/getCovid19SidoInfStateJson'
    params = {
        'serviceKey': 'LWBFUlqDXNuZDTsQ+iegJLALUyCNcGP6RaqECjc3L7jD3/CWizVpvqNPIHbd+anLmaBHvGwYitxoVSsq9DiR/A==',
        'pageNo': '1',
        'numOfRows': 10,
        'startCreateDt': startCreateDt,  # '20210514',
        'endCreateDt': endCreateDt,  # '20210514'

    }

    res = requests.get(url, params=params)

    dict_data = xmltodict.parse(res.text)
    json_data = json.dumps(dict_data)

    dict_data = json.loads(json_data)

    totalCount = dict_data['response']['body']['totalCount']
    if totalCount == "0":
        return False

    data = dict_data['response']['body']['items']['item']
    data.reverse()
    return data


class ActionCovid19Tracker(Action):

    def name(self) -> Text:
        return "action_covid19_Tracker"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        entities = tracker.latest_message['entities']
        print(entities)

        for e in entities:
            if e['entity'] == 'date':
                name = e['value']

            if name == "today":
                message = "today covid 19 people..."
            if name == "yesterday":
                message = "yesterday covid 19 people..."
            if name == "two days ago":
                message = "two days ago covid 19 people..."
            if name == "three days ago":
                message = "three days ago covid 19 people..."
            if name == "four days ago":
                message = "four days ago covid 19 people..."
            if name == "five days ago":
                message = "five days ago covid 19 people..."
            if name == "six days ago":
                message = "six days ago covid 19 people..."
            if name == "a week ago":
                message = "a week ago covid 19 people..."

        dispatcher.utter_message(text=message)

        return []


class ActionCovid19Answer(Action):

     def name(self) -> Text:
         return "action_covid19_locationanswer"



     def run(self, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

         entities = tracker.latest_message['entities']
         print(entities)
         for e in entities:
             if e['entity'] == "location":
                 location = e['value']

         for e in entities:
             if e['entity'] == 'date':
                 name = e['value']

             if name == "today":
                 now = date.today()
                 now_str = now.strftime("%Y%m%d")
                 print(now_str)

                 # 오늘 날짜로 요청해라
                 data = get_corona_data(now_str, now_str)
                 print(data)


                 for i in data:
                     if i["gubunEn"] == location.title():
                         print(i)
                         message = "location: " + i["gubun"] + "date: " + i["stdDay"] + "\nConfirmed:  " + i[
                             "defCnt"] + "\nThe death toll: " + i["deathCnt"] + "\nIsolation: " + i[
                                       "isolIngCnt"] + "\nRelease: " + i["isolClearCnt"] + "\nNew: " + i["incDec"]
                         dispatcher.utter_message(text=message)

             if name == "yesterday":
                 now = date.today()
                 yesterday = now - timedelta(days=1)
                 yesterday_str = yesterday.strftime("%Y%m%d")
                 print(yesterday_str)

                 data = get_corona_data(yesterday_str, yesterday_str)
                 print(data)


                 for i in data:
                     if i["gubunEn"] == location.title():
                         print(i)
                         message1 = "location: " + i["gubun"] + "date: " + i["stdDay"] + "\nConfirmed:  " + i[
                             "defCnt"] + "\nThe death toll: " + i["deathCnt"] + "\nIsolation: " + i[
                                        "isolIngCnt"] + "\nRelease: " + i["isolClearCnt"] + "\nNew: " + i["incDec"]

                         dispatcher.utter_message(text=message1)



         return []


class ActionCovid19Answer2(Action):

    def name(self) -> Text:
        return "action_covid19_QuestionAnswer"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        entities = tracker.latest_message['entities']
        print(entities)

        for e in entities:
            if e['entity'] == 'questions':
                name = e['value']

        if name == "symptoms":
                message = "Fever, dry cough, fatigue, and loss of appetite are the most common symptoms. " \
                          "The first symptoms may be a sore throat and a dry cough.Headache, confusion, runny nose, diarrhea, nausea, and vomiting may occur, but are less common (< 10%)." \
                          " Loss of taste and smell occurs." \
                          "Shortness of breath is reported in 30-40% of patients. If pneumonia develops, shortness of breath may become much worse and require hospital treatment with oxygen or even mechanical ventilation."
        if name == "prevention" or "prevent":
                message = "home quarantine as much as possible" \
                          "Keep 6 feet (2 meters) away from others in public Wash your hands often, " \
                          "especially after being in public or after sneezing or coughing " \
                          "Wash your hands immediately after coughing into a tissue or elbow " \
                          "Avoid touching your eyes, nose or mouth with unwashed hands " \
                          "Cleaning and disinfecting frequently touched surfaces (e.g. tables, doorknobs, knobs, phones, keyboards)" \
                          "Wear a cloth face covering when in public places, around people other than those with whom you live in your home, or when it is difficult to maintain social distancing measures. " \
                          "Maintain a distance of about 6 feet (about 2 meters) between yourself and others. Cloth face coverings are not a substitute for social distancing."

        if name == "recur" or "Relapse":
                message = "Regardless of whether or not symptoms develop, " \
                          "people infected with COVID-19 begin to produce antibodies to the virus within a few days after infection, but it is not yet possible to determine whether " \
                          "these antibodies provide immunity to virus re-infection, and how long if immunity develops. It's too early. Studies done on other coronavirus infections in humans, including the strains that cause the common cold, " \
                          "and studies done after the first SARS outbreak in the early 2000s have shown that people lose immunity to these coronaviruses months or years later. Under the present circumstances, " \
                          "the best conclusion doctors can make is that most infected people will have some degree of immunity, " \
                          "but probably not for life."

        if name == "social distancing":
                message = "<Rule 1> Take 3-4 days off if you are sick" \
                          "<Rule 2> Keep a healthy distance between you and your arms" \
                          "<Rule 3> Wash your hands for 30 seconds, coughing into your sleeve" \
                          "<Rule 4> Ventilate at least twice a day and disinfect" \
                          "<Rule 5> Even if the distance is far away, the heart is close"

        if name == "information":
                message = "Corona virus (CoV) is a virus that can infect humans and various animals, and is an RNA virus with a gene size of 27 to 32 kb."
                if name == "social distancing":
                    message1 = "<Rule 1> Take 3-4 days off if you are sick" \
                          "<Rule 2> Keep a healthy distance between you and your arms" \
                          "<Rule 3> Wash your hands for 30 seconds, coughing into your sleeve" \
                          "<Rule 4> Ventilate at least twice a day and disinfect" \
                          "<Rule 5> Even if the distance is far away, the heart is close"
                    dispatcher.utter_message(text=message1)


        dispatcher.utter_message(text=message)

        return []