from haunt.client import HauntClient

client = HauntClient()


@client.bind
def hello():
    print("i was called")


client.mount(path="test.html", title="Haunt", debug=False, gui="qt")
