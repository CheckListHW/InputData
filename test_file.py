from mvc.Model.map import Map, ExportRoof

if __name__ == '__main__':
    data = Map()
    data.load_from_json('C:/Users/KosachevIV/PycharmProjects/InputData/base.json')
    export = ExportRoof(data)
    print('finish')
