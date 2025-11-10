from langchain_text_splitters import RecursiveCharacterTextSplitter

text = """
“Debut author and single mother sells children’s book for £100,000.” So announced a July 1997 headline in the Guardian newspaper touting the record-breaking windfall novice writer Joanne Kathleen Rowling earned for Harry Potter and the Philosopher’s Stone. It was the first in a planned series of novels about a powerful young wizard drawn into an epic battle of good versus evil, and the article posited that Harry “could assume the same near-legendary status as Roald Dahl’s Charlie, of chocolate factory fame.”

Nearly two and a half decades later, it’s a safe bet that children are more well-versed in the adventures of Harry and his plucky best mates Ronald Weasley and Hermione Granger than they are with Dahl’s Charlie Bucket. Rowling’s chara

cters have become a part of the global cultural lexicon thanks to the fantasy juggernaut. It seems nearly everyone’s heard of the Boy Who Lived. “The characters were so funny and so very specific, and the world came alive on the page,” says Anne Rouyer, supervising young adult librarian at the New York Public Library. “It was one of those books you could sell to any kid, whether they were [an avid] reader or a reluctant reader. Even now, kids just discover them, and they’re just as magical as they were 25 years ago.”

Looking back, few would have imagined the extent to which that first book’s young protagonist—an English orphan whisked away from a life of drudgery and abuse into a world where staircases move, paintings talk, and owls deliver the mail—would become a dominant force in popular culture the world over.

"""

splitter = RecursiveCharacterTextSplitter(
    chunk_size = 300,
    chunk_overlap = 0,
)

results = splitter.split_text(text)

for  index , result in enumerate(results):
    print(f"line {index} : {result}")   