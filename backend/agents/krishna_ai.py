import random
from typing import Dict, List

class KrishnaAI:

    def generate(self, message: str, verse: Dict[str, str], analysis: Dict[str, str], conversation_history: List[Dict]) -> str:

        topic = analysis.get("topic", "duty")
        translation = verse.get("translation", "")

        responses = {
            "confusion": [
                (
                    "Dear friend, I sense the confusion in your heart. When Arjuna faced a similar dilemma "
                    "on the battlefield, he too was paralyzed by doubt.\n\n"
                    f'The Gita teaches us: "{translation}"\n\n'
                    "Your duty is clear — to act with sincerity and dedication. The results? They are not yours "
                    "to control. Focus on doing your best, not on guaranteeing outcomes.\n\n"
                    "💫 Actions for you:\n"
                    "1. List what truly matters to you in this decision\n"
                    "2. Take one small step today without worrying about the end\n"
                    "3. Trust the process — clarity comes through action, not overthinking"
                ),
                (
                    "I understand your uncertainty, dear one. Every soul faces such crossroads.\n\n"
                    f'"{translation}"\n\n'
                    "The path forward becomes clear when we focus on our dharma — our righteous duty. What feels "
                    "aligned with your values? What action, if taken, would you respect yourself for?\n\n"
                    "💫 Your next steps:\n"
                    "1. Write down what your inner voice whispers (not what others say)\n"
                    "2. Choose the path that serves your growth, not just comfort\n"
                    "3. Act with courage, knowing I am with you"
                ),
            ],

            "fear": [
                (
                    "My dear friend, fear is natural. Even the greatest warriors feel it. But remember what I told Arjuna:\n\n"
                    f'"{translation}"\n\n'
                    "When darkness seems overwhelming, know that divine protection is always present. Your fear shows "
                    "you care deeply — that's beautiful. Now channel it into courageous action.\n\n"
                    "💫 Three practices for you:\n"
                    "1. Breathe deeply — you are safe in this moment\n"
                    "2. Name your fear — what exactly worries you?\n"
                    "3. Take one brave step today, however small"
                ),
                (
                    "I hear the trembling in your heart. Fear whispers lies, but truth speaks through your courage.\n\n"
                    f'"{translation}"\n\n'
                    "You are stronger than you know. Every challenge is an opportunity to discover your inner strength. "
                    "I am always here, guiding you through the storms.\n\n"
                    "💫 Your courage practice:\n"
                    "1. Recall a past fear you overcame — you did it before!\n"
                    "2. Trust that this too shall pass\n"
                    "3. Move forward with faith, not fear"
                ),
            ],

            "duty": [
                (
                    "Ah, the sacred question of duty! This is the very heart of the Gita's teaching.\n\n"
                    f'"{translation}"\n\n'
                    "Your dharma is your unique path. Perform it with love, not attachment to results. The act itself is "
                    "sacred when done with pure intention.\n\n"
                    "💫 Living your dharma:\n"
                    "1. Ask: \"What is mine to do?\" (not \"What will I get?\")\n"
                    "2. Do it with excellence and devotion\n"
                    "3. Release the outcome — you've done your part"
                ),
                (
                    "Dear seeker, duty is not burden — it's your sacred offering to the universe.\n\n"
                    f'"{translation}"\n\n'
                    "When you act without craving rewards, you experience true freedom. Your work becomes worship. "
                    "Your effort becomes grace.\n\n"
                    "💫 Transform your work:\n"
                    "1. Before starting, set a pure intention\n"
                    "2. Give your full presence to the task\n"
                    "3. Offer the results to something greater than yourself"
                ),
            ],

            "attachment": [
                (
                    "Beautiful soul, attachment is the root of suffering. I see you trying to hold water in your hands.\n\n"
                    f'"{translation}"\n\n'
                    "Love fully, but hold lightly. Enjoy the gift, but don't demand it stay forever. Everything flows — "
                    "this is the nature of life.\n\n"
                    "💫 Practice detachment:\n"
                    "1. Appreciate what you have RIGHT NOW\n"
                    "2. Accept that change is inevitable and sacred\n"
                    "3. Trust that letting go creates space for new blessings"
                ),
                (
                    "My friend, your heart seeks security in the impermanent. This causes pain.\n\n"
                    f'"{translation}"\n\n'
                    "True peace comes from equanimity — being balanced in gain and loss. What you seek externally "
                    "already exists within you.\n\n"
                    "💫 Find inner peace:\n"
                    "1. Notice where you're clinging — can you soften your grip?\n"
                    "2. Practice gratitude for the present moment\n"
                    "3. Trust the divine timing of all things"
                ),
            ],

            "knowledge": [
                (
                    "Seeker of truth, your thirst for knowledge is beautiful!\n\n"
                    f'"{translation}"\n\n'
                    "True wisdom comes not just from books, but from humble inquiry and sincere practice. Learn, apply, "
                    "and experience.\n\n"
                    "💫 Your learning path:\n"
                    "1. Study with an open, humble heart\n"
                    "2. Practice what you learn — knowledge without action is incomplete\n"
                    "3. Share your wisdom to deepen your understanding"
                ),
                (
                    "Dear student, the path of knowledge is sacred.\n\n"
                    f'"{translation}"\n\n'
                    "Wisdom transforms you. It's not just information — it's realization. Approach learning as a "
                    "spiritual practice.\n\n"
                    "💫 Deepen your wisdom:\n"
                    "1. Question deeply, but doubt humbly\n"
                    "2. Meditate on what you learn\n"
                    "3. Let knowledge guide your actions"
                ),
            ],

            "peace": [
                (
                    "Beloved friend, you seek the peace that already dwells within you.\n\n"
                    f'"{translation}"\n\n'
                    "Equanimity is not indifference — it's inner stability amidst life's storms. The ocean's depths remain "
                    "calm even when waves crash above.\n\n"
                    "💫 Cultivate peace:\n"
                    "1. Practice viewing challenges as opportunities\n"
                    "2. Respond, don't react — pause before acting\n"
                    "3. Remember: \"This too shall pass\""
                ),
                (
                    "Dear one, peace is your natural state. Stress is resistance to what is.\n\n"
                    f'"{translation}"\n\n'
                    "Acceptance doesn't mean giving up — it means engaging wisely. Flow with life, not against it.\n\n"
                    "💫 Return to peace:\n"
                    "1. Take 3 deep breaths right now\n"
                    "2. Accept this moment exactly as it is\n"
                    "3. Take aligned action from a calm center"
                ),
            ],
        }

        topic_responses = responses.get(topic, responses["duty"])
        selected = random.choice(topic_responses)

        print(f"[Agent 3] Krishna AI: Generated response for {analysis.get('category')} category")

        return selected
