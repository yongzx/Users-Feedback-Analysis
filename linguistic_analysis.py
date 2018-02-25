import json
from textblob.classifiers import NaiveBayesClassifier
from collections import Counter

data = json.load(open("frames.json"))

def get_final_utterances_from_user(data):
	"""
	Function:
	Retrieve all the final messages sent by the user.

	Input: a dictionary which contains the conversations between a user and the wizard.
	Output: a list, final_utterance, which stores lists of final messages sent by the user in each dialogue.
			messages_by_users[i] contains the final utterance sent by the user in the ith dialogue.

	Algorithm:
	1. For all the dialogues, first store the messages by a user into the list conversation.
 	2. Then append the list conversation to the list messages_by_users.
 	3. Use the list comprehension to extract the last message in each list of messages in the list messages_by_users.
	"""

	messages_by_users = []
	for i in range(len(data)):
		conversation = [data[i]['turns'][j]['text'] for j in range(0, len(data[i]['turns']), 2)]
		messages_by_users.append(conversation)

	final_utterance = [message[len(message) - 1] for message in messages_by_users]
	return final_utterance

messages_by_users = get_final_utterances_from_user(data)


def get_messages_from_user_negated(data):
	"""
	Input: a dictionary which contains the conversations between a user and the wizard.
	Output: a list, messages_by_users_negated, which stores lists of final messages sent by the user who does not book the vacation in each dialogue.
			messages_by_users[i] contains the final utterance sent by the user in the ith dialogue.

	Algorithm:
	1. If the last turn of the conversation is the user. If it isn't then the user must reply at the second to last turn, because
	   the wizard always reply one message after the user.
	2. Check if the user affirms the suggestion of hotel or flight tickets given by the wizard.
	3. If the user confirms the suggestion, do nothing.
	4. Otherwise, stores the message (in which the user doesn't accept the suggestion by the wizard )to the list messages_by_users_negated
	"""
	messages_by_users_negated = []
	for i in range(len(data)):
		if data[i]['turns'][-1]["author"] == "user":
			if 'acts_without_refs' in data[i]['turns'][-1]['labels'] and data[i]['turns'][-1]['labels']['acts_without_refs'] and data[i]['turns'][-1]['labels']['acts_without_refs'][0]['name'] == 'affirm':
				continue
			else:
				messages_by_users_negated.append(data[i]['turns'][-1]['text'])
		else:
			if 'acts_without_refs' in data[i]['turns'][-2]['labels'] and data[i]['turns'][-2]['labels']['acts_without_refs'] and data[i]['turns'][-2]['labels']['acts_without_refs'][0]['name'] == 'affirm':
				continue
			else:
				messages_by_users_negated.append(data[i]['turns'][-2]['text'])

	return messages_by_users_negated

messages_by_users_negated = get_messages_from_user_negated(data)

def final_utterance_appreciation_analysis(final_utterance):
	"""
	Input: A list of final utterances by the user.
	Output: The percentage of the people expressing appreciation at the end of the conversation.

	Algorithm:
	1. Create a training set and a validation set of conversation which are manually classified into "appreciation" and "nonappreciation"
	   The differentiation criteria is based on the existence of the words of gratitude.
	2. Train the Naive Bayesian classifier algorithm using the training set.
	3. If the accuracy of the classifier algorithm in classifying the validation dataset into "appreciation" and "nonappreciation",
	   apply the algorithm to all the list final_utterance using a for loop.
	4. Use a dictionary data structure during the loop to store the number of people who express gratitude and who do not express gratitude.
	5. Calculate the percentage of people who express gratitude.

	How the Native Bayesian Classifier Algorithm from TextBlob Package Works:

	For training dataset:
	In order to find the probability for classifying the sentence with a label of "appreciation" and "nonappreciation",
	the algorithm first removes all the meaningless stop words such as "the" and "a" in the sentence.
	Then it calculates the frequency of the remaining tokens and creates a likelihood table that maps the tokens (which are the features)
	to the probability of the token being labelled as "appreciation" and "nonappreciation".

	For a new sentence, it removes all the meaningless stop words and calculate the probability of the sentence being "appreciation"
	or "nonappreciation" based on the 'naive' assumption that all features are independent, given the label:
	|                       P(label) * P(f1|label) * ... * P(fn|label)
	|  P(label|features) = --------------------------------------------
	|                                         P(features)

	"""

	classified_dict = {"appreciation": 0, "non-appreciation": 0}

	train = [('Very well. How about the price for the trip to Essen?', 'nonappreciation'),
	         ("I'd like to book the Cairo package. Thank you!", 'appreciation'),
	         ('oh heck yeah!! economy - I need the money', 'nonappreciation'),
	         ('Then I will take it!', 'nonappreciation'),
	         ('Awesome!!! Thanks!!!', 'appreciation'),
	         ('What??? :disappointed:', 'nonappreciation'),
	         ('Yes do that', 'nonappreciation'),
	         ('Thank you kindly!', 'appreciation'),
	         ('Ok, thank you for your time anyways', 'appreciation'),
	         ('thank you very much for your patience you are an absolute gem','appreciation'),
	         ('Thank you so much!', 'appreciation'),
	         ('Lots of swanky hotels to choose from! Well, based on length of trip, that one to SL sounds like a great deal. I think I wanna go ahead with booking that', 'nonappreciation'),
	         ('Uh huh', 'nonappreciation'),
	         ('Jerusalem to Kingston. I swear if I have to repeat myself again then I will sue', 'nonappreciation'),
	         ('Ok, thanks anyway','appreciation'),
	         ('Looking to go from San Francisco to MArseille. ', 'nonappreciation'),
	         ('Book me for September 18 to 22. Let me know if its more than 2800 because thats all I can afford', 'nonappreciation'),
	         ('duuuude. ah\nwhat about Ciudad Juarez', 'nonappreciation'),
	         ('Well what if I leave the 8th', 'nonappreciation'),
	         ('Ok :+1: we out', 'nonappreciation'),
	         ('Yes!!!!!', 'nonappreciation'),
	         ('ok fine lets do it, business class please', 'nonappreciation'),
	         ('WOE IS ME, FOR I HAVE NOT', 'nonappreciation'),
	         ('ah damn', 'nonappreciation'),
	         ('okay bye', 'nonappreciation'),
	         ('Yikes. Ok Buenos Aires it is\nBook it please\nBusiness class', 'nonappreciation'),
	         ('shit yassss we goin in. Book it for us, please.', 'nonappreciation'),
	         ('well, this is rather disappointing we cannot spend our family vacation near the airport. i wont be booking anything today in this case, goodbye', 'nonappreciation'),
	         ('Thanks! Very excited!', 'appreciation'),
	         ('NOT GOOD', 'nonappreciation'),
	         ("you're a lifesaver", "appreciation"),
	         ('ah. if i could book, i would book this one. well thanks for your time, ill come back next year and save my vacation days for a trip to San Diego.', "appreciation"),
	         ('Great, thanks a lot!', "appreciation"),
	         ("WHAT!?!?! Ugh, kill me now. Okkay fine. I'll look somewhere else.", "nonappreciation"),
	         ("I guess that sound okay, I'll take it", "nonappreciation"),
	         ("Ok, that's fine\nBook it", "nonappreciation"),
	         ('I like the sound of that one. Heart of the city would be better than near a mall.\nLets book business class in Buenos Aires.', "nonappreciation"),
	         ('cool bye', "nonappreciation"),
	         ("let's book :wink:", "nonappreciation"),
	         ('Done, booked! Thanks!', 'appreciation'),
	         ('Okay will consider it and get back to you, thanks!', 'appreciation'),
	         ('DOPE. book it', 'nonappreciation'),
	         ('Hmm. Okay well im just gonna take the information you gave me and discuss it with my wife before booking something she might not enjoy. Thanks for the help!', 'appreciation'),
	         ('Thanks! You were a great help!', 'appreciation'),
	         ('i said 2.5 wasnt good enough', 'nonappreciation'),
	         ('No thats the last straw, we are taking our business elsewhere', 'nonappreciation'),
	         ('Thanks :slightly_smiling_face:', 'appreciation'),
	         ('Hi Do you fly from Ulsan to London??', 'nonappreciation'),
	         ('Ok then leave from Beijing', 'appreciation'),
	         ('i need to get away from a little longer than that one. so lets book vancouver please and thanks', "appreciation"),
	         ("Let's book Valencia. Pleasure doing business with you.", "appreciation"),
	         ('Thank you bot.', "appreciation"),
	         ('No worries, thanks!', "appreciation"),
	         ("That sucks. I'll look somewhere else", "nonappreciation"),
	         ('I am giving you one last time to you your job. you better tread carefully here, my friend,\nCairo to Porto Alegre or I will raise hell', "nonappreciation"),
	         ('Bye. And thanks for nothing.', "nonappreciation"),
	         ("Yes, I'll take it. Thank you", "nonappreciation"),
	         ('no there are 7 of us', "nonappreciation"),
	         ('for 712.00 it sounds like a very nice deal I will book flight on August 26 for 6 days. Thank you for your help.', 'appreciation'),
	         ('3.5 it is then. lets book it', 'nonappreciation'),
	         ('but fine, book it', 'nonappreciation'),
	         ('no can do', "nonappreciation"),
	         ('Thank you very much.', "nonappreciation"),
	         ('gracias!', "appreciation"),
	         ("Perfect! I'll book it", "nonappreciation"),
	         ('Do you do flights leaving from Tel Aviv?', "nonappreciation"),
	         ('that seem good, i will book! Gracias!', "appreciation"),
	         ("No it's alright! thanks though!", "appreciation"),
	         ('okay well its crucial i get there from Fortaleza so I will call someone else', "nonappreciation"),
	         ('how is that possible', "nonappreciation"),
	         ('Well what about in Goiania.?','nonappreciation'),
	         ('ok no thats not good enough im going elsewhere', "nonappreciation"),
	         ('amazing! thanks!', "appreciation"),
	         ('Lets do Business class', "nonappreciation"),
	         ("Oh Okay well i'll look somewhere else. Thanks anyway.", "appreciation"),
	         ('you dont have any flights to birmingham yeah i find that pretty freakin hard to believe', "nonappreciation"),
	         ('This is HORRIBLE', "nonappreciation"),
	         ("yes, you're right.. thank you", "appreciation"),
	         ('ok thanks so much', "appreciation"),
	         ('what if i changed the dates. sept 2 and 23', "nonappreciation"),
	         ('Thank you, but I will go use another service that can better satisfy my escapist fantasies', "appreciation"),
	         ("I really want a spa. If you have nothing to offer with a spa, I'll shop around then.", 'nonappreciation'),
	         ('Oh dear, thats quite above our 3 thousand dollar budget.', 'nonappreciation'),
			 ('dope! thanks', 'appreciation'),
			 ('No worries! Bye!', 'nonappreciation'),
			 ('Ok Lets lock in San Diego', "nonappreciation"),
			 ("You're great", 'appreciation'),
			 ('ok. book it out of Milan please', 'nonappreciation)'),
			 ('ill go for Ciudad Juarez', "nonappreciation"),
			 ('Thank you wozbot!', "appreciation"),
			 ('yes please', "nonappreciation"),
			 ("Usually I wouldn't want to be caught dead in a 3.5 star hotel, but I'm short on time here. Get us on that trip, business class", "nonappreciation"),
			 ('GREAT Thanks!!!!!!!!', "appreciation"),
			 ("I think I'll stick to the 11 day package in Belem at Las Flores, seems like the best deal and it had a good user rating. Let's book that one.", "nonappreciation"),
			 ('thnx', "appreciation"),
			 ('no it HAS to be baltimore and it HAS to be perfect. thanks anyways', "appreciation"),
			 ("Perfect! I'll book it", "nonappreciation"),
			 ("That's it?", "nonappreciation"),
			 ('I shall take the 5 star package!', "nonappreciation"),
			 ('thank you so much', "appreciation"),
			 ('YOU ARE RUINING MY MARRIAGE', "nonappreciation")]

	validation = [('Yes chief', "appreciation"),
				 ("Thanks! I'm sure it will be amazinggg", "appreciation"),
				 ("Weeeelllll this is a no brainer, I 'll just leave the next day and save a whole lotta money! Can you book this for me right away so I don't lose it?", "nonappreciation"),
				 ("Ok I'll book the package with 8 days in Pittsburgh from August 17th to the 24th. Thank you.", "appreciation"),
				 ('Thanks - will do', "appreciation"),
				 ('Killing it! thank', "appreciation"),
				 ('Thanks, you too', "appreciation"),
				 ('thank you wozbot :slightly_smiling_face: toodles', "appreciation"),
				 ('spectacular book please', "nonappreciation"),
				 ("Well, I reckon I'll just book this one.", "nonappreciation"),
				 ("yea so I've heard... send me to Paris then", 'nonappreciation'),
				 ('Fortaleza\n5 stars', "nonappreciation"),
				 ('I guess I can increase my budget by 1000', 'nonappreciation'),
				 ('ok see ya', "nonappreciation"),
				 ('leaving from anywhere??', "nonappreciation"),
				 ("That's it! Thank you so so much :):):)", "appreciation"),
				 ('Done. Book it.', "nonappreciation"),
				 ('Great, sounds perfect. Thank you.', "appreciation"),
				 ('Thats all i had my heart set on!!', "nonappreciation"),
				 ("That sounds like the better hotel. Can't be too cautious travelling by myself for the first time! I will book that deal in an economy class ticket, I'm not ready for business class YET, need to pass that bar exam!",  "nonappreciation"),
				 ('Then I will take my search elsewhere', "nonappreciation"),
				 ('Ya thanks', "appreciation"),
				 ('Thank you, glad to be going back so soon', "appreciation"),
				 ('well okay I can always take the tram in to the city. I will book that one.', "nonappreciation"),
				 ('This is hopeless', "nonappreciation"),
				 ('Great, thank you. I will most certainly book my next vacation with you.', "appreciation"),
				 ('thank youuuu', "appreciation"),
				 ('Lock it down', "nonappreciation"),
				 ("Please help! My lovely parents have been married fof 20 years and they've never taken a trip together. I'm thinking of getting them out of town Sept 6 to 9\nyou got anything good for 2 adults leaving sao paulo, for under 2400?", "nonappreciation"),
				 ('we can also go to Kochi', "nonappreciation"),
				 ('no but we can stay for 9 days instead of 3', "nonappreciation"),
				 ('thanks you!', "appreciation"),
				 ('Just under budget. ok bye now', "nonappreciation"),
				 ('thankyou', "appreciation"),
				 ('can you tell me the price and nearby attractions?', "nonappreciation"),
				 ('1 adult', "nonappreciation"),
				 ('San Jose to Porto Alegre please. oh it needs to be between sept 18 to 22', "nonappreciation"),
				 ('Ok sold! please enter a booking for us', "nonappreciation"),
				 ('I can leave from Tel aviv and I want to go to San Jose with 7 adults for 2500', "nonappreciation"),
				 ('Well what about in Goiania.?', "nonappreciation"),
				 ('you are being unhelpful just answer yes or no, is it near a park or beach?', "nonappreciation"),
				 ('thak you', "appreciation"),
				 ('I shall take the 5 star package!', "nonappreciation"),
				 ('Okay but what if I leave from Naples instead. Can you get me to Manas from Naples?', "nonappreciation"),
				 ("I'm a woman! Try to find something 9000 or less if you can.", "nonappreciation"),
				 ("That's perfect.", "nonappreciation"),
				 ('ok. fine. I have a 4500 $ budjet and I will star as long as that money lasts. thx', "appreciation"),
				 ('sure fine flexible actually no i dont wanna go any more', "nonappreciation"),
				 ("No, unfortunately I can't. Guess I'll just take a staycation this time :disappointed: Thanks anyway", "appreciation"),
				 (" I'll book this one. Thank you, friend!", "appreciation"),
				 ('No we can only go to Porto... or Porto. Thanks.', "appreciation")]

	cl = NaiveBayesClassifier(train) # train the Naive Bayesian Classifier algorithm
	if cl.accuracy(validation) > 0.90: # check if the accuracy of the Naive Bayesian Classifier algorithm in classifying the validation data set is greater than 90%.
		cl.update(validation)	# update the Naive Bayesian Classifier algorithm with the validation data set.

		for m in final_utterance:
			if cl.classify(m) == "appreciation":
				classified_dict["appreciation"] += 1
			else:
				classified_dict["non-appreciation"] += 1

	# calculate the percentage of people expressing appreciation
	return "{}% people express appreciation.".format(float(classified_dict["appreciation"] / (float(classified_dict["appreciation"] + classified_dict["non-appreciation"]))) * 100)


print final_utterance_appreciation_analysis(messages_by_users)
print final_utterance_appreciation_analysis(messages_by_users_negated)