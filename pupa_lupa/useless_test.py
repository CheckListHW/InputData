def tracert(**kwargs):
    edit_lay(**kwargs)

def edit_lay(**kwargs):
    print(kwargs)
    print(kwargs.get('value'))
    print(kwargs.get('v1alue'))

if __name__ == "__main__":
    tracert(value='asd')

