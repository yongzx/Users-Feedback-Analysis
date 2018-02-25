import json
from collections import Counter 
from matplotlib import pyplot as plt
import numpy as np

data = json.load(open("frames.json"))

def mean(L):
    """
    Input: a list of real numbers
    Output: the mean value of the list of numbers

    The mean value of a data set is the sum of all the numbers in the list divided by the number of numbers in the list.
    """

    return round(sum(L) / len(L), 2) #round to precision of 2

def data_range(L):
    """
    Input: a list of real numbers
    Output: the range of the values in the list.

    The range of a data set is the difference between the largest and smallest number in the list.
    I sort the list into ascending order of the numbers. The range is therefore the difference between the first and last
    element in the list.
    """
    L.sort()
    return L[-1] - L[0]

def median(L):
    """
    Input: a list of real numbers
    Output: the median of the values in the list.

    The median of a data set is the "middle" value that separates the higher half of the ordered data sample from the lower half.
    If the list has an odd number of element, the median is at the ( (total number of elements - 1) / 2 )th position.
    If the list has an even number of element, the median is in between ( (total number of elements / 2) + 1 )th and
    ( total number of elements / 2 )th elements, which is the ((total number of elements / 2) - 1)th element and
    ( total number of elements / 2)th in a python list.
    """
    L.sort()

    if len(L) % 2:
        return L[len(L) // 2]

    return (L[len(L) // 2] + L[len(L) // 2 - 1]) / 2

def std_dev(L):
    """
    Input: a list of real numbers
    Output: the standard deviation of the values of the list.

    The standard deviation is a population standard deviation instead of sample standard deviation
    because I am not interested in generalizing the standard deviation of this sample to a larger population of 
    humans sending messages over the chatbox.
    ("Standard Deviation", n.d.).

    The population standard deviation of a data set is the root-mean square of the deviations of the values in the data set from the mean value.

    Reference: Standard Deviation. (n.d.) Retrieved from https://statistics.laerd.com/statistical-guides/measures-of-spread-standard-deviation.php
    """
    mean_val = mean(L)
    deviation = []
    for n in L:
        deviation.append((n - mean_val) ** 2)
    return round((sum(deviation) / (len(L))) ** 0.5, 2) #round to precision of 2

def mode(L):
	"""
	Input: a list of real numbers
    Output: the mode of the values of the list.

    Use a Counter dictionary to map a distinct value to its the frequency in the list.
    Output the value with the largest frequency
	"""
	counter = Counter(L)
	max_count = max(counter.values())
	mode = [k for k,v in counter.items() if v == max_count]

	if len(mode) == 1:
		return mode[0]

	return mode

def get_messages_from_user(data):
	"""
	Function:
	Retrieve all the messages sent by the user. 

	Input: a dictionary which contains the conversations between a user and the wizard.
	Output: a list, messages_by_users, which stores lists of messages sent by the user in each dialogue.
			messages_by_users[i] contains the list of messages sent by the user in the ith conversation.
	
	Algorithm:
	For all the dialogues, first store the messages by a user into the list conversation.
 	Then append the list conversation to the list messages_by_users.
	"""

	messages_by_users = []
	for i in range(len(data)):	
		# access to the ith conversation using data[i]
		# it is the user who initiates the conversation so we start from the range of 0
		# the user and the wizard takes turn to send messages, so we can use a step of 2. 
		conversation = [data[i]['turns'][j]['text'] for j in range(0, len(data[i]['turns']), 2)] 
		messages_by_users.append(conversation)

	return messages_by_users


def get_messages_from_wizards(data):
	"""
	Function:
	Retrieve all the messages sent by the wizard. 

	Input: a dictionary which contains the conversations between a user and the wizard.
	Output: a list, messages_by_users, which stores lists of messages sent by the wizard in each dialogue.
			messages_by_users[i] contains the list of messages sent by the wizard in the ith conversation.
	
	Algorithm:
	For all the dialogues, first store the messages by a wizard into the list conversation.
 	Then append the list conversation to the list messages_by_wizards.
	"""
	messages_by_wizards = []
	for i in range(len(data)):
		# access to the ith conversation using data[i]
		# the wizard replies to the user's message, so we start from the range of 1.
		# the user and the wizard takes turn to send messages, so we can use a step of 2. 
		conversation = [data[i]['turns'][j]['text'] for j in range(1, len(data[i]['turns']), 2)]
		print(conversation)
		messages_by_wizards.append(conversation)

	return messages_by_wizards

def words_count_analysis(messages, role):
	"""
	Input: A list of messages. 
		   messages[i] denotes the ith conversation, which is a list that stores the messages sent by the user or by the wizard in the conversation.
	Output: a tuple which contains mean, median, mode, range and standard deviation of the total number of words in a conversation (either by the user or by the wizard).
	
	Algorithm:
	1. For each list conversation, which stores the messages sent from one end in the particular conversation, split all the sentences into words.
	2. Count all the words in a particular conversation and append it to the list word_count_per_conversation.
	3. Plot a histogram of the number of words sent by the person in a conversation.
	4. Use mean(), median(), mode(), data_range(), std_dev() to find the mean, median, mode, range and standard deviation of the total number of words in a conversation (either by the user or by the wizard).
	"""
	word_count_per_conversation = []
	for conversation in messages:
		word_count = 0
		for message in conversation:
			words = message.split(" ")
			word_count += len(words)
		word_count_per_conversation.append(word_count)

	color = "yellow" if role == "User" else "blue"
	plt.hist(word_count_per_conversation, color="{}".format(color),
			 bins=[i for i in range(min(word_count_per_conversation), max(word_count_per_conversation), 20)],
			 edgecolor='black', linewidth=1.2)
	plt.ylabel("Frequency")
	plt.xlabel("Number of Words Sent by {} in a Conversation".format(role))
	plt.xticks([0, 50, 100, 150, 200, 250, 300, 350, 400, 450, 500])
	plt.yticks([0,50,100,150,200,250])
	plt.show()
	
	return mean(word_count_per_conversation), median(word_count_per_conversation), \
			mode(word_count_per_conversation), data_range(word_count_per_conversation), \
			std_dev(word_count_per_conversation)

def messages_count_analysis(messages, role):
	"""
	Input: A list of messages. 
		   messages[i] denotes the ith conversation, which is a list that stores the messages sent by the user or by the wizard in the conversation.
	Output: a tuple which contains mean, median, mode, range and standard deviation of the number of messages in a conversation (either by the user or by the wizard).
	
	Algorithm:
	1. For each list conversation, which stores the messages sent from one end in the ith conversation, find out the number of the messages in the particular conversation using len().
	2. Append the number of messages in the particular conversation to the list messages_count_per_conversation
	3. Plot a histogram of the number of messages sent by the person in a conversation.
	4. Use mean(), median(), mode(), data_range(), std_dev() to find the mean, median, mode, range and standard deviation of the number of messages in a conversation (either by the user or by the wizard).
	"""
	messages_count_per_conversation = []
	for conversation in messages:
		messages_count_per_conversation.append(len(conversation))

	color = "yellow" if role == "User" else "blue"
	plt.hist(messages_count_per_conversation, color="{}".format(color),
			 bins=[i for i in range(min(messages_count_per_conversation), max(messages_count_per_conversation))],
			 edgecolor='black', linewidth=1.2)
	plt.ylabel("Frequency")
	plt.xlabel("Number of Messages Sent by {} in a Conversation".format(role))
	plt.show()
	
	return mean(messages_count_per_conversation), median(messages_count_per_conversation), \
			mode(messages_count_per_conversation), data_range(messages_count_per_conversation), \
			std_dev(messages_count_per_conversation)

def words_per_message_analysis(messages, role):
	"""
	Input: A list of messages.
		   messages[i] denotes the ith conversation, which is a list that stores the messages sent by the user or by the wizard in the conversation.
	Output: a tuple which contains mean, median, mode, range and standard deviation of the number of words in a message (sent either by the user or by the wizard).

	Algorithm:
	1. For each list conversation, which stores the messages sent from one end in the particular conversation, split each sentence into words.
	2. Find the number of the words in each sentence using len() and append the value to the list words_per_message.
	3. Plot a histogram of the number of words sent by the person in a message
	4. Use mean(), median(), mode(), data_range(), std_dev() to find the mean, median, mode, range and standard deviation of the number of words in a message (sent either by the user or by the wizard).
	"""
	words_per_message = []
	for conversation in messages:
		for message in conversation:
			words = message.split(" ")
			words_per_message.append(len(words))

	# plot histogram
	color = "yellow" if role == "User" else "blue"
	plt.hist(words_per_message, color="{}".format(color),
			 bins=[i for i in range(min(words_per_message), max(words_per_message), 5)],
			 edgecolor='black', linewidth=1.2)
	plt.xticks([0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110])
	plt.yticks([0,500,1000,1500,2000,2500,3000,3500])
	plt.ylabel("Frequency")
	plt.xlabel("Number of Words Sent by {} in a Message".format(role))
	plt.show()

	return mean(words_per_message), median(words_per_message), \
			mode(words_per_message), data_range(words_per_message), \
			std_dev(words_per_message)


messages_by_users = get_messages_from_user(data)
messages_by_wizards = get_messages_from_wizards(data)
print(words_count_analysis(messages_by_users, "User"))
print(messages_count_analysis(messages_by_users, "User"))
print(words_per_message_analysis(messages_by_users, "User"))
print(words_count_analysis(messages_by_wizards, "Wizard"))
print(messages_count_analysis(messages_by_wizards, "Wizard"))
print(words_per_message_analysis(messages_by_wizards, "Wizard"))

def pearson_coefficient(X, Y):
    """
    :param list1: numpy array of values
    :param list2: numpy array of values. The number of values matches the number of values in list1
    :return: Pearson's correlation coefficient value

    Formula:
                   SUM( (X[i] - mean of X) * (Y[i] - mean of Y) )
    r = ----------------------------------------------------------------------
         (V SUM( (X[i] - mean of X)**2 ) ) * (V SUM( (Y[i] - mean of Y)**2 ) )

    Algorithm:
    1.  Find the means of the two lists.
    2.  Calculate the numerator of the formula, which is the sum of product of the differences between each element
        in the two lists and their respective means of the two lists
    3.  Calculate the denominator of the formula, by first calculating the sum of squared differences of each element
        in the first list.
    4.  Then calculate the sum of squared differences of each element in the second list.
    5.  Calculate the denominator by multiplying the square root of results from step 3 and 4.

    Reference: Computing the Pearson Correlation Coefficient.
    Retrieved from http://www.stat.wmich.edu/s216/book/node122.html
    """

    def mean(L):
        # calculate the mean value of the list of data
        return sum(L) / len(L)

    mean_x = mean(X)
    mean_y = mean(Y)
    numerator = 0
    denominator1 = 0
    denominator2 = 0
    for i in range(len(X)):
        numerator += (X[i] - mean_x) * (Y[i] - mean_y)  # sum of product of differences
        denominator1 += (X[i] - mean_x) ** 2
        denominator2 += (Y[i] - mean_y) ** 2

    return numerator / (denominator1 ** 0.5 * denominator2 ** 0.5)


def least_square_regression_line(X, Y):
    """
    :param X: numpy array of values for x axis.
    :param Y: numpy array of values for y axis. The number of values matches the number of values in list1
    :return: tuple of gradient and intercept for the least square regression line

    Formulae:
    Gradient = pearson coefficient * standard deviation of data set of y values / standard deviation of data set of x values
    Intercept = mean of data set of y values - gradient * mean of data set of x values

    Reference: Calculating the Least Squares Regression Line
    Retrieved from http://www.stat.wmich.edu/s216/book/node126.html
    """

    def mean(L):
        # calculate the mean value of the list of data
        return sum(L) / len(L)

    def std_dev(L):
        # calculate the standard deviation of the list of data
        mean_val = mean(L)
        deviation = []
        for n in L:
            deviation.append((n - mean_val) ** 2)
        return (sum(deviation) / (len(L) - 1)) ** 0.5

    gradient = pearson_coefficient(X, Y) * std_dev(Y) / std_dev(X)
    intercept = mean(Y) - gradient * mean(X)

    return gradient, intercept


def r2(X, Y):
    """
    :param X: numpy array of values.
    :param Y: numpy array of values. The number of values matches the number of values in list1
    :return: R^2 value

    Formulae:
    SSR = SUM ( ( y-value from regression line of X[i] - mean of Y)**2 )
    SSTO = SUM ( (Y[i] - mean of Y)**2 )
    R^2 = SSR / SSTO

    Algorithm:
    1.  Use for-loop to calculate the SSR, sum of squared differences between y-value from the least squared regression
        line equation using x-value from the list X and the mean of Y.
    2.  Use for-loop to calculate the SSTO, sum of squared differences between y-value from the list Y and the mean
        of Y
    3.  Calculate R^2 by dividing SSR by SSTO.

    Reference: The Coefficient of Determination, r-squared
    Retrieved from https://onlinecourses.science.psu.edu/stat501/node/255
    """

    def mean(L):
        # calculate the mean value of the list of data
        return sum(L) / len(L)

    gradient, intercept = least_square_regression_line(X, Y)

    ssr = 0
    ssto = 0
    for i in range(len(Y)):
        ssto += (Y[i] - mean(Y)) ** 2
        ssr += ((gradient * X[i] + intercept) - mean(Y)) ** 2

    return ssr / ssto

def correlation_word_count(users, wizards):
	"""
	Input: The list of messages sent by users. The list of messages sent by wizards.
	Output: The tuple of Pearson's coefficient of correlation and R^2 value.
	
	Algorithm:
	1. For each list conversation in the list of messages sent by the user, split all the sentences into words.
	2. Count all the words in a particular conversation and append it to the list word_count_per_conversation_users.
	3. Repeat step 1 and 2 for the list of messages sent by the wizard, and the value of the number of words in the conversation is stored in the list word_count_per_conversation_wizards
	4. Plot a scatterplot diagram of the number of words typed by the user against the wizard in the conversation.
	5. Calculate the Pearson's coefficient of correlation and R^2 value of the two lists using pearson_coefficient() and r2().
	"""
	word_count_per_conversation_users = []
	for conversation in users:
		word_count = 0
		for message in conversation:
			words = message.split(" ")
			word_count += len(words)
		word_count_per_conversation_users.append(word_count)

	word_count_per_conversation_wizards = []
	for conversation in wizards:
		word_count = 0
		for message in conversation:
			words = message.split(" ")
			word_count += len(words)
		word_count_per_conversation_wizards.append(word_count)

	# plot scatterplot diagram with regression line
	data, = plt.plot(word_count_per_conversation_wizards, word_count_per_conversation_users, 'o', markersize=2, label="data")
	gradient, intercept = least_square_regression_line(word_count_per_conversation_wizards, word_count_per_conversation_users)
	line, = plt.plot(word_count_per_conversation_wizards, intercept + gradient * np.array(word_count_per_conversation_wizards),
					 label="regression line")
	plt.legend(handles=[data, line])
	plt.xlabel("Number of Words Typed by the Wizard in the Conversation")
	plt.ylabel("Number of Words Typed by the User in the Conversation")
	plt.show()

	return gradient, intercept, pearson_coefficient(word_count_per_conversation_wizards, word_count_per_conversation_users), r2(word_count_per_conversation_wizards, word_count_per_conversation_users)

def correlation_avg_num_words_per_message(users, wizards):
	"""
	Input: The list of messages sent by users. The list of messages sent by wizards.
	Output: The tuple of Pearson's coefficient of correlation and R^2 value.
	
	This function investigates if the number of words in a message sent by the wizard affects the number of words sent by the user.
	Therefore, the first message of the user is ignored because the length of the user's first message is not affected by the wizard. 

	Algorithm:
	1. For ith conversation in the list of messages sent by the user, split each sentence into words.
	2. Find the number of the words in each sentence using len() and append the value to the initialized list words_per_message_users.
	3. Repeat step 1 and 2 for the list of messages sent by the wizard, and the value of the number of words in the conversation is stored in the list words_per_message_wizards.
	4. Use pop(0) to ignore the first message of the user.
	5. If the number of messages sent by the wizard in a conversation is longer than that sent by the user, append 0 to the list words_per_message_users to signify that the user does not reply to the wizard.
	6. Add the values in the list words_per_message_users and words_per_message_wizards to words_per_message_users_final and words_per_message_wizards_final respectively
	7. Plot a scatterplot diagram of the number of words in a message sent by the user against the wizard in the conversation.
	8. Calculate the Pearson's coefficient of correlation and R^2 value of the two lists words_per_message_users_final and words_per_message_wizards_final using pearson_coefficient() and r2().
	"""
	words_per_message_users_final = []
	words_per_message_wizards_final = []
	for i in range(len(users)):
		words_per_message_users = []
		for message in users[i]:
				words = message.split(" ")
				words_per_message_users.append(len(words))

		words_per_message_wizards = []
		for message in wizards[i]:
			words = message.split(" ")
			words_per_message_wizards.append(len(words))

		# This function investigates if the number of words in a message sent by the wizard affects the number of words sent by the user.
		# Therefore, the first message of the user is ignored because the length of the user's first message is not affected by the wizard. 
		words_per_message_users.pop(0)

		if len(words_per_message_wizards) == len(words_per_message_users) + 1:
			# if the number of messages sent by the wizard in a conversation is longer than that sent by the user,
			# append 0 to the list words_per_message_users to signify that the user does not reply to the wizard.
			words_per_message_users.append(0)
		
		words_per_message_users_final += words_per_message_users
		words_per_message_wizards_final += words_per_message_wizards

	# plot scatterplot diagram with regression line
	data, = plt.plot(words_per_message_wizards_final, words_per_message_users_final, 'o', markersize = 2, label = "data")
	gradient, intercept = least_square_regression_line(words_per_message_wizards_final, words_per_message_users_final)
	line, = plt.plot(words_per_message_wizards_final, intercept + gradient * np.array(words_per_message_wizards_final), label="regression line")
	plt.legend(handles=[data, line])
	plt.xlabel("Number of Words in the Message sent by the Wizard in a Conversation")
	plt.ylabel("Number of Words in the Message sent by the User in a Conversation")
	plt.show()

	return gradient, intercept, pearson_coefficient(words_per_message_users_final, words_per_message_wizards_final), r2(words_per_message_users_final, words_per_message_wizards_final)


def correlation_message_count(users, wizards):
	"""
	Input: The list of messages sent by users. The list of messages sent by wizards.
	Output: The tuple of Pearson's coefficient of correlation and R^2 value.
	
	Algorithm:
	1. For each list conversation in the list of messages sent by the user, find out the number of the messages in the particular conversation using len().
	2. Append the number of messages in the particular conversation to the list messages_count_per_conversation_users
	3. Repeat step 1 and 2 for the list of messages sent by the wizard, and the number of the messages per conversation is stored in the list messages_count_per_conversation_wizards.
	4. PLot a scatterplot diagram of the number of messages sent by the user against the wizard in a conversation.
	5. Calculate the Pearson's coefficient of correlation and R^2 value of the two lists using pearson_coefficient() and r2().
	"""
	messages_count_per_conversation_users = []
	for conversation in users:
		messages_count_per_conversation_users.append(len(conversation))

	messages_count_per_conversation_wizards = []
	for conversation in wizards:
		messages_count_per_conversation_wizards.append(len(conversation))

	# plot scatterplot diagram with regression line
	data, = plt.plot(messages_count_per_conversation_wizards, messages_count_per_conversation_users, 'o', markersize = 2, label = "data")
	gradient, intercept = least_square_regression_line(messages_count_per_conversation_wizards, messages_count_per_conversation_users)
	line, = plt.plot(messages_count_per_conversation_wizards, intercept + gradient * np.array(messages_count_per_conversation_wizards), label="regression line")
	plt.legend(handles=[data, line])
	plt.xlabel("Number of Messages sent by the Wizard in a Conversation")
	plt.ylabel("Number of Messages sent by the User in a Conversation")
	plt.show()

	return gradient, intercept, pearson_coefficient(messages_count_per_conversation_users, messages_count_per_conversation_wizards), r2(messages_count_per_conversation_users, messages_count_per_conversation_wizards)


print("correlation of word count: ", correlation_word_count(messages_by_users, messages_by_wizards))
print("correlation of number of words per message: ", correlation_avg_num_words_per_message(messages_by_users, messages_by_wizards))
print("correlation of messages: ", correlation_message_count(messages_by_users, messages_by_wizards))