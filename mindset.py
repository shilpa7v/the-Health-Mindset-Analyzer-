import random
import matplotlib.pyplot as plt
from gtts import gTTS
import os

def main():
    print("Welcome to the Health Mindset Analyzer!")
    name = input("What's your name? ")
    age = input("How old are you? ")
    print(f"Hello, {name}! Let's assess your health mindset.")
    print("Please answer the following questions with a number from 1 to 5, where:")
    print("1 - Strongly Disagree, 2 - Disagree, 3 - Neutral, 4 - Agree, 5 - Strongly Agree")
    
    # Shuffle the questions
    questions = [
        "I prioritize my physical health.",
        "I regularly engage in physical exercise.",
        "I eat a balanced and nutritious diet.",
        "I prioritize my mental health.",
        "I actively manage my stress levels.",
        "I prioritize getting enough sleep.",
        "I seek out information on healthy living."
    ]
    random.shuffle(questions)
    
    answers = []
    for i, question in enumerate(questions, 1):
        while True:
            answer = input(f"{question} How much do you agree with this statement? (1-5): ")
            if answer.isdigit() and 1 <= int(answer) <= 5:
                answers.append(int(answer))
                break
            else:
                print("Invalid input! Please enter a number between 1 and 5.")

    language = input("Select your preferred language (en/es/ta/te/kn): ").lower()

    feedback_text, speech_text, mindset_changed = give_feedback(answers, language, name)
    print(feedback_text)
    print(speech_text)
    
    # Save speech as an MP3 file and play it
    save_and_play_speech(speech_text, language)

    # Generate and display pie chart
    generate_pie_chart(answers)
    
    # Get user's thoughts
    user_thoughts = input("Share your thoughts on your health mindset (separated by commas): ")
    thoughts = user_thoughts.split(", ")

    # Provide feedback based on user's thoughts
    provide_feedback(thoughts, language)

    # Display whether mindset changed or not
    if mindset_changed:
        print("Your health mindset seems to have changed.")
    else:
        print("Your health mindset remains the same.")

def save_and_play_speech(text, language):
    tts = gTTS(text=text, lang=language)
    tts.save("output.mp3")
    os.system("start output.mp3")

def generate_pie_chart(answers):
    labels = ['Strongly Disagree', 'Disagree', 'Neutral', 'Agree', 'Strongly Agree']
    counts = [answers.count(i) for i in range(1, 6)]
    explode = (0.1, 0, 0, 0, 0)  # explode 1st slice
    colors = ['#ff9999','#66b3ff','#99ff99','#ffcc99','#c2c2f0']
    
    plt.figure(figsize=(8, 6))
    plt.pie(counts, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140)
    plt.title('Distribution of Responses')
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.show()
    
def give_feedback(answers, language='en', name=""):
    feedback = {
        'en': {
            'health_focused': f"{name}, your mindset seems to be focused on health. Here are some tips to maintain a healthy lifestyle:",
            'less_health_focused': f"{name}, your mindset seems to be less focused on health. Here are some tips to improve your health mindset:"
        },
        'es': {
            'health_focused': f"{name}, tu enfoque parece estar centrado en la salud. Aquí hay algunos consejos para mantener un estilo de vida saludable:",
            'less_health_focused': f"{name}, tu enfoque parece estar menos centrado en la salud. Aquí hay algunos consejos para mejorar tu mentalidad de salud:"
        },
        'ta': {
            'health_focused': f"{name}, உங்கள் நம்பிக்கை உடல் நலமுக்கான செய்திகளுக்காக அன்புள்ள உறவின் வாழ்க்கையை காத்திருக்கும் தீர்வுகள்:",
            'less_health_focused': f"{name}, உங்கள் நம்பிக்கை உடல் நலமுக்கான செய்திகளுக்காக அன்புள்ள உறவின் வாழ்க்கையை மேம்படுத்த சில குறிப்புகள்:"
        },
        'te': {
            'health_focused': f"{name}, మీ ధ్యానం ఆరోగ్యంపెట్టుబడి పై ఉంది. ఆరోగ్యకర జీవన శైలిని నిర్వహించడానికి కొన్ని సూచనలు:",
            'less_health_focused': f"{name}, మీ ధ్యానం ఆరోగ్యంపెట్టుబడి పై లేదు. మీ ఆరోగ్య మైండ్సెట్ను మెరుగుపరచడానికి కొన్ని సూచనలు:"
        },
        'kn': {
            'health_focused': f"{name}, ನಿಮ್ಮ ಮನಸ್ಸು ಆರೋಗ್ಯಕ್ಕೆ ಹೆಚ್ಚು ಮುಖ್ಯವಾಗಿಲ್ಲ. ನಿಮ್ಮ ಆರೋಗ್ಯ ಮನಸ್ಸನ್ನು ಮೇಲೆ ತರಲು ಕೆಲವು ಸಲಹೆಗಳು:",
            'less_health_focused': f"{name}, ನಿಮ್ಮ ಮನಸ್ಸು ಆರೋಗ್ಯಕ್ಕೆ ಹೆಚ್ಚು ಮುಖ್ಯವಾಗಿಲ್ಲ. ನಿಮ್ಮ ಆರೋಗ್ಯ ಮನಸ್ಸನ್ನು ಮೇಲೆ ತರಲು ಕೆಲವು ಸಲಹೆಗಳು:"
        }
    }

    language_feedback = feedback.get(language, feedback['en'])

    healthy_count = sum(answer in [4, 5] for answer in answers)

    if healthy_count >= len(answers) / 2:
        feedback_text = language_feedback['health_focused']
        speech_text = (
            "Your mindset seems to be focused on health. Here are some tips to maintain a healthy lifestyle:\n"
            "• Eat a balanced diet rich in fruits, vegetables, and whole grains.\n"
            "• Exercise regularly, aiming for at least 30 minutes of activity most days.\n"
            "• Get enough sleep, aiming for 7-9 hours per night.\n"
            "• Manage stress through relaxation techniques like meditation or yoga."
        )
    else:
        feedback_text = language_feedback['less_health_focused']
        speech_text = (
            "Your mindset seems to be less focused on health. Here are some tips to improve your health mindset:\n"
            "• Start by incorporating small, positive changes into your daily routine.\n"
            "• Set achievable health goals and track your progress.\n"
            "• Surround yourself with supportive individuals who prioritize health.\n"
            "• Educate yourself about the benefits of a healthy lifestyle."
        )

    return feedback_text, speech_text, healthy_count >= len(answers) / 2

def provide_feedback(thoughts, language):
    positive_responses = [
        "Your honesty is appreciated! Remember to take some time for yourself and engage in activities that bring you joy.",
        "It's great that you're aware of your feelings. Remember to practice self-care and reach out for support if needed."
    ]
    negative_responses = [
        "It's okay to feel stressed sometimes. Remember to take breaks and engage in activities that help you relax, like watching your favorite show or going for a walk.",
        "Thank you for being honest about how you're feeling. Remember, it's important to prioritize self-care and take steps to manage your stress levels."
    ]

    for idx, thought in enumerate(thoughts, 1):
        if "stressed" in thought.lower():
            print(random.choice(negative_responses))
        else:
            print(random.choice(positive_responses))

        speech_text = random.choice(positive_responses) if "stressed" not in thought.lower() else random.choice(negative_responses)
        tts = gTTS(text=speech_text, lang=language)
        tts.save(f"output_{idx}.mp3")
        os.system(f"start output_{idx}.mp3")

if __name__ == "__main__":
    main()
