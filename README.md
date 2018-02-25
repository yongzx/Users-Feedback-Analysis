# Analysis of Users' Feedbacks to Virtual Assistant

### Resources
`frames.json` : dataset released by a Microsoft company named Maluuba that contains 1369 conversations between two people over a chatbox. In the conversation, one person played the role of the user who is planning a vacation, and the other, known as the wizard, simulated the role of virtual assistant and provided the information about hotels and flights to the user.

`datanalysis.py` : A Python script that analyze the lengths and the number of messages sent between the two users.

`linguistic_analysis.py` : A Python script that uses NaiveBayesClassifier to analyze whether the users appreciate the help from the virtual assistant.


### Findings

**The result for the number of messages sent by the user and by the wizards shows that on average, the conversation has approximately 14 messages in total.** This signifies that the task of retrieving necessary information such as hotel and plane tickets for planning the vacation can be completed within 14 messages on average. 

**The wizard types a longer response** because the wizard provides comprehensive information about the suggestions of hotels and the plane tickets that fit into the criteria of the user.

There is a moderately high positive coefficient of correlation between the number of words typed by the user and by the wizard in a conversation. But it does not necessarily mean that the longer reply by the wizard causes the user to type a longer message or vice versa. **This is shown by the low coefficient of correlation between the number of words in the user’s message and the wizard’s message.**

The Naïve Bayesian classifier algorithm classified the validation set of the final utterances of the user into appreciation and non-appreciation categories with an **accuracy of 90.2%**. This accuracy value is high enough for the trained algorithm to classify the rest of the dataset. By updating the algorithm and applying it to the Maluuba’s dataset, it was found that **56.6% of the users expressed words of appreciation at the end of conversation.** In addition, even when the user was failed to plan the vacation because there is no hotel or flight which meets the user’s criteria, 57% of the user still expressed their appreciation.