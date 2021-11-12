import json

try:
    from run import app
    import unittest

except Exception as e:
    print(("Some Modules are missig {}".format(e)))


class Transport_Test(unittest.TestCase):
    greeting = ['Hello!, How can I help you ?', 'Good to see you again!, How can I help you ?',
                'Hi there,  How can I help you ?', 'Hello!, How can I help you ?']

    travel = ["travel"]
    schedule = ["schedule"]
    complaint = ["complaint"]
    reserve = ["reserve"]

    def test_1_index(self):
        tester = app.test_client(self)
        response = tester.get("/")
        status_code = response.status_code
        self.assertEqual(status_code, 200)  # check API call work properly
        self.assertEqual(response.content_type, "application/json")  # check the return content is application/json
        self.assertTrue(b'"members":["Member","Hello Sandaruwan"]' in response.data)  # check correct data is returned

    def test_2_reply(self):
        tester = app.test_client(self)
        # calling backend API
        response_greaating = tester.post("/reply", json={'msg': 'hi'})
        response_travel = tester.post("/reply", json={'msg': "could you tell me the best way to get to"})
        response_schedule = tester.post("/reply", json={'msg': "are there any trains from colombo to galle tommorow"})
        response_complaint = tester.post("/reply", json={'msg': "the bus is moving too slow"})
        response_reserve = tester.post("/reply", json={'msg': "make a reservation"})

        status_code = response_greaating.status_code
        self.assertEqual(status_code, 200)  # check API call work properly

        self.assertEqual(response_greaating.content_type,
                         "application/json")  # check the return content is application/json

        # response data for each backend request
        data_greeting = json.loads(response_greaating.data)
        data_travel = json.loads(response_travel.data)
        data_schedule = json.loads(response_schedule.data)
        data_complaint = json.loads(response_complaint.data)
        data_reserve = json.loads(response_reserve.data)

        self.assertTrue(data_greeting['members'] in Transport_Test.greeting)
        self.assertTrue(data_travel['members'] in Transport_Test.travel)
        self.assertTrue(data_schedule['members'] in Transport_Test.schedule)
        self.assertTrue(data_complaint['members'] in Transport_Test.complaint)
        self.assertTrue(data_reserve['members'] in Transport_Test.reserve)


if __name__ == "__main__":
    unittest.main()
