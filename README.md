First install ollama from the website

Go into the folder and create conda environment
-> conda create -n ollama python 3.11
-> conda activate ollama

Testing chat text response from the ollama mistral model
-> ollama run mistral
-> python app.py

Question: Why is the sky blue?(Inside the code app.py)
output: The color of the sky appears blue due to a phenomenon called Rayleigh scattering. As sunlight travels to Earth, it interacts with molecules and particles in the Earth's atmosphere. Blue light has a shorter wavelength and gets scattered more easily than other colors, such as red or yellow. This scattering scatters the blue light in all directions, making the sky appear blue during a clear day. At sunrise and sunset, the sky takes on hues of red, pink, and orange due to a different type of scattering called scattering by larger particles like dust and water droplets.

Testing llava modal with a image(image.jpeg)
-> ollama run llava
-> python multimodal.py
![image](https://github.com/chakri15797/ollama-ui-app/assets/31991608/9b0ff3d6-0e6c-4513-9431-440a6110f88a)
Question: What is in the image?
Output: The image shows a moment from a cricket match. A cricketer is in the middle of a shot, having just released the ball towards the wicketkeeper, who is waiting to catch it. Another player with bat in hand is ready for the next play. They are both wearing cricket gear and the player holding the bat has the number 10 on his jersey. The cricketer is also wearing a blue helmet with a white chin guard. In the background, there's an umpire standing behind the stumps, closely observing the play. The setting suggests this is a professional cricket match, possibly from the Indian Premier League (IPL), given the uniform of the players and the atmosphere around the ground. 

Give a Html link and ask questions to ollama
-> python ui.py
open link http://127.0.0.1:7860 in the browser and start chatting with your AI modal.
