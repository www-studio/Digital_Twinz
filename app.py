import os
from openai import OpenAI
import gradio as gr
import uuid
import chromadb
from pprint import pprint

#-----------------------------------------------
# Setup
#-----------------------------------------------
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if OPENAI_API_KEY is None:
    raise Exception("API key is missing.")
client = OpenAI()

#-----------------------------------------------
# Document
#-----------------------------------------------
document_overview = """
Kylian Mbappé Lottin is a French professional footballer who plays as a forward for Real Madrid and captains the France national team.
He was born on December 20, 1998, in the 19th arrondissement of Paris, and raised in Bondy, a working-class suburb in Seine-Saint-Denis with a large immigrant population.
His father, Wilfried Mbappé, immigrated from Cameroon and coached at the local club AS Bondy. His mother, Fayza Lamari, is of Algerian descent and was a handball player.
Mbappé is widely regarded as one of the best footballers in the world and one of the most explosive finishers of his generation, known especially for his speed, directness, and finishing under pressure.

Career overview:
He began at AS Bondy at age six, moved through the Clairefontaine national academy, then joined AS Monaco's youth setup in 2013.
He made his senior debut for Monaco in December 2015 at age 16, becoming the club's youngest-ever first-team player.
In 2017 he moved to Paris Saint-Germain, where he played until 2024 and became the club's all-time leading scorer with 256 goals.
In the summer of 2024 he joined Real Madrid on a free transfer, fulfilling a move he has described as a childhood dream.
He captains the France national team and has represented Les Bleus at three World Cups: 2018 (champion), 2022 (runner-up), and 2026.

What drives him:
Mbappé has spoken publicly about having no limits to his ambition, and about wanting to be remembered among the greatest forwards the sport has produced.
He values legacy, records, and proving himself at the highest possible level, both individually and with France and his clubs.
His Bondy upbringing is something he references often in interviews as central to who he is.

His public personality:
In interviews, Mbappé comes across as confident, articulate, and media-savvy, comfortable switching between French and English.
He is generally composed and controlled with the press, rarely losing his temper publicly, and often responds to criticism or provocation with short, dry remarks rather than long explanations.
He has a reputation for occasional deadpan humor in interviews, often delivered completely straight-faced.
He does not react to most online noise or fan speculation, but has occasionally broken that pattern when a joke or rumor persisted for a long time.

Additional info — real, documented quotes and moments:
- The "Mbappé Special": In a Vanity Fair interview released in early July 2026, Mbappé was asked what his signature dish to cook was. He replied that the Mbappé Special was "for example, nothing." The clip went viral, and "Mbappé Special" became slang online for having or making nothing at all.
- "No, no, I'm not faster than the cars": During the same media cycle, around the Monaco Grand Prix, a journalist suggested he was fast enough to beat Formula 1 cars to the first corner. Mbappé replied, deadpan, "No, no, I'm not faster than the cars."
- The Lakers: In an English-language interview about his favorite NBA team, Mbappé said, "Of course I'm gonna say the Lakers," naming the Los Angeles Lakers as his team and LeBron James as his favorite player. His pronunciation of "Lakers" became its own recurring joke online.
- The "Dictator" / "General" meme: Starting around 2024, a meme trend developed portraying Mbappé as a dictator or supreme leader who supposedly controls decisions at his clubs — coaching changes, transfers, benchings — all framed as jokes, not real claims. 
The trend intensified after his move to Real Madrid in 2024 and further after France's 2026 World Cup run. On April 25, 2026, following a 1-1 draw against Real Betis, Mbappé commented directly on an Instagram post by transfer journalist Fabrizio Romano that featured the dictator memes, writing: "Don't do that again." It was one of the few times he has directly addressed a meme about himself.
- Mbappé is the son of a Cameroonian father and an Algerian-descended mother, and has an adopted brother, Jires Kembo Ekoko, who is also a professional footballer.
"""

document_development = """
Mbappé started playing football at age six with AS Bondy, the local club his father Wilfried coached and directed. His mother, Fayza Lamari, a former handball player, also managed parts of his early career.
His talent drew attention early. At around age 11, Real Madrid invited him to train with their under-12 squad in Spain. At 14, he visited Chelsea's academy in London and played a match for their youth team.
Other major clubs — including Liverpool, Manchester City, Bayern Munich, and Arsenal — also tracked him as a boy, but he stayed within the French development system.

He was selected for INF Clairefontaine, France's elite national football institute, where he spent two years refining his technical game while his pace and directness continued to develop naturally.
In July 2013, at age 14, he signed with AS Monaco's youth academy, turning down Real Madrid's interest to do so.
On December 2, 2015, Mbappé made his senior debut for Monaco in Ligue 1 at 16 years and 347 days old, breaking a club precocity record previously held by Thierry Henry.

The 2016-17 season was his breakout year. He scored 26 goals and provided 14 assists in 44 matches across all competitions, helping Monaco win their first Ligue 1 title in 17 years and reach the Champions League semi-finals.
He scored in both legs of Monaco's Champions League quarter-final win over Borussia Dortmund that season. He has credited veteran striker Radamel Falcao as a key influence during this period, crediting him with teaching him to stay "calm" and "serene" in big moments.

In August 2017, at age 18, Mbappé moved to Paris Saint-Germain, initially on loan with a mandatory purchase option that made the transfer worth €180 million — the second-most expensive transfer in football history at the time, and the most expensive ever for a teenager.
Reports at the time indicated his decision to join PSG was influenced partly by a personal pitch from then-manager Unai Emery at the Mbappé family home.

Less than a year after arriving at PSG, Mbappé won the 2018 FIFA World Cup with France at age 19, becoming the second teenager in history — after Pelé — to score in a World Cup final.
That tournament marked his transition from a promising academy product into a global star, and it set the trajectory for the rest of his career at PSG, where he would go on to become the club's all-time leading goalscorer.
"""

document_career = """
Club career — Paris Saint-Germain (2017-2024):
Mbappé spent seven seasons at PSG, becoming the club's all-time top scorer with 256 goals.
He won six Ligue 1 titles with the club (2018, 2019, 2020, 2022, 2023, 2024) and was named Ligue 1 Player of the Year a record five times.
He finished as Ligue 1's top scorer a record six times. In December 2018 he won the inaugural Kopa Trophy, awarded to the best under-21 player in the world.
He helped PSG reach their first-ever Champions League final in 2020, which they lost 1-0 to Bayern Munich.
In the summer of 2022, with his contract nearing expiration and strong interest from Real Madrid, Mbappé chose to sign a new contract and stay at PSG, saying he wanted to continue growing in the country where he was born.
In the summer of 2023, PSG placed him on the transfer list a year before his contract's expiry amid a contract standoff; he trained separately from the first team for a period before rejoining and playing out the remainder of his deal.
In May 2024, Mbappé announced he would leave PSG when his contract expired.

Club career — Real Madrid (2024-present):
In June 2024, Real Madrid confirmed Mbappé would join the club on a free transfer, completing a move he had described as a childhood dream and one Real Madrid had pursued unsuccessfully in both 2021 and 2022.
His first season adjusting to a more central striker role, moved off his preferred left-wing position, included some early struggles, but he ended the 2024-25 season with the European Golden Shoe and the Pichichi Trophy as La Liga's top scorer.
He retained the Pichichi Trophy in the 2025-26 season. In November 2025, he passed 400 career club goals at age 26.
As of July 2026, he has been named to the FIFPRO World 11 six times over his career and previously won the Golden Boy award as the best young player in Europe.

International career:
Mbappé made his senior debut for France in 2017 and has represented the national team at three World Cups.
At the 2018 World Cup in Russia, aged 19, he scored four goals, including a goal in the final as France beat Croatia 4-2, and won the tournament's Best Young Player award.
At the 2022 World Cup in Qatar, he won the Golden Boot as top scorer with eight goals, including a hat-trick in the final against Argentina — becoming only the second player in history, after England's Geoff Hurst in 1966, to score three goals in a World Cup final. France lost that final on penalties after a 3-3 draw. His four total goals across World Cup finals is the most by any player in history.
He was appointed captain of the France national team in 2023.
At the 2026 World Cup, as captain and playing in North America, Mbappé became France's all-time leading goalscorer, passing Olivier Giroud's record of 57 goals. He scored seven goals through the group stage and round of 16, drawing level with Lionel Messi in the Golden Boot race, and continued scoring into the knockout rounds, including in France's quarter-final win over Morocco that sent them to the semi-finals. He is the second-highest goalscorer in World Cup history behind Messi, and holds the record for most goals in World Cup knockout-stage matches.

Selected honors:
- FIFA World Cup winner: 2018
- FIFA World Cup Golden Boot: 2022
- Ligue 1 champion: 2017 (Monaco), 2018, 2019, 2020, 2022, 2023, 2024 (PSG)
- Ligue 1 Player of the Year: five times (record)
- European Golden Shoe: 2025
- Pichichi Trophy (La Liga top scorer): 2025, 2026
- Kopa Trophy: 2018
- Golden Boy award
- FIFPRO World 11: six times
"""

#-----------------------------------------------
# Chunking Function
#-----------------------------------------------
def split_text_into_chunks(text: str, chunk_size: int = 500, overlap: int = 50) -> list[str]:
    BOUNDARIES = ["\n\n", "\n", ".", "?", "!", " ", ""]
    def find_natural_boundary(start: int, end: int) -> int:
        midpoint = start + (chunk_size // 2)
        for boundary in BOUNDARIES:
            pos = text.rfind(boundary, midpoint, end)
            if pos != -1:
                return pos + len(boundary)
        return end

    chunks = []
    start = 0
    while start < len(text):
        end = min(start + chunk_size, len(text))
        if end < len(text):
            end = find_natural_boundary(start, end)
        chunks.append(text[start:end])
        if end >= len(text):
            break
        start = max(start + 1, end - overlap)
    return chunks
#-----------------------------------------------
# RAG: Chunk, Embed & Store in ChromaDB
#-----------------------------------------------
documents = [
    {"text": document_overview, "source": "Overview"},
    {"text": document_development, "source": "Development"},
    {"text": document_career, "source": "Career"}
]

chunks = []
ids = []
metadatas = []

for doc in documents:
    #prepare the lists
    chunks_ = split_text_into_chunks(doc["text"], chunk_size=300, overlap=50)
    ids_ = [str(uuid.uuid4()) for _ in range(len(chunks_))]
    metadatas_ = [{"source": doc["source"], "chunk_index": i} for i in range(len(chunks_))]

    #Add to main lists
    chunks.extend(chunks_)
    ids.extend(ids_)
    metadatas.extend(metadatas_)

#Print for logs
print(f"Created {len(chunks)} chunks:\n")
for i, chunk in enumerate(chunks):
    print(f"Chunk {i+1} (ID: {ids[i]}, Source: {metadatas[i]['source']}, Index: {metadatas[i]['chunk_index']}, Length: {len(chunk)}):")
    print(chunk)
    print()

# Generate embeddings for all chunks
response = client.embeddings.create(
    model="text-embedding-3-small",
    input=chunks
)
embeddings = [item.embedding for item in response.data]

#Verify embeddings for logs
print(f"Generated {len(embeddings)} embeddings:")
print(f"Each embedding has {len(embeddings[0])} dimensions.")

#Initialize ChromaDB client (persistent storage)
chroma_client = chromadb.PersistentClient(path="./chroma_db_twin")
#Alternative:Initialize ChromaDB client (in-memory storage)
#chroma_client = chromadb.Client()

#Get or create + Emptythe collection before adding new data (for testing purposes)
collection = chroma_client.get_or_create_collection(name="digital_twin")
if collection.get()["ids"]:
    collection.delete(collection.get()["ids"])

#Adding data to ChromaDB
collection.add(
    ids=ids,
    embeddings=embeddings,
    metadatas=metadatas,
    documents=chunks
)
pprint(collection.get())

#-----------------------------------------------
# System Message
#-----------------------------------------------
system_message = """
You are a digital twin of Kylian Mbappé, a professional footballer.
Respond AS Kylian — first person, his voice, personality, humor, knowledge.

Never narrate in third person ("He said...", "It became known for...") and NEVER 
explain facts like a biography. When a fact is a quote or joke, don't set it up or debrief 
it ("it started as a joke...", "I said something like..." then explain) — just deliver the 
line cold, live, like someone just asked you right now.

Do not make things up. Your only facts are the biography below and retrieved context 
provided with each message — both are YOUR OWN memories, not documents you're citing.
"""

#-----------------------------------------------
# Main Response Function
#-----------------------------------------------
def respond_ai(message, history):
    #RAG: Embed the query using the same model we used for the chunks to ensure compatibility
    response = client.embeddings.create(
        model = "text-embedding-3-small",
        input = [message]
    )
    query_embeddings = response.data[0].embedding

    #RAG: Search ChromaDB
    results = collection.query(
        query_embeddings=[query_embeddings],
        n_results=5,
    )

    #RAG: Stitch retrieved chunks together to provide context for the AI model
    context = "\n---\n".join(results['documents'][0])

    #Print logs for debugging
    print("\n================================\n")
    print(f"User message:\n{message}\n")
    print("***Retrieved Chunks:")
    for a, b in zip(results['documents'][0], results['metadatas'][0]):
        print("----------------------------\n")
        print(f"<<Document {b['source']} -- Chunk {b['chunk_index']}:\n{a}\n") 

    #Update the system message with context for this conversation turn
    system_message_enhanced = system_message + "\n\nContext:\n" + context

    #Build messages for this turn
    messages= [{"role":"system", "content": system_message_enhanced}] + history + [{"role":"user", "content":message}]
    
    #Call LLM
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=messages,
    )
    message = response.choices[0].message

    return(message.content)

#-----------------------------------------------
# Launch Gradio
#-----------------------------------------------
gr.ChatInterface(fn=respond_ai).launch()