def ReadSetting():
    import ast
    file = open('./setting', 'r')
    contents = file.read()
    dictionary = ast.literal_eval(contents)
    return dictionary
