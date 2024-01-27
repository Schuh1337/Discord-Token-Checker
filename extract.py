validPath = 'valid.txt'
extractedPath = 'extracted.txt'

with open(validPath, 'r') as file:
    tokenList = file.read().splitlines()

extractedTokens = []

for i, token in enumerate(tokenList):
    if not token.strip() or len(token.split(':')) != 3:
        continue
    
    email, password, extractedToken = token.split(':')
    extractedTokens.append(extractedToken)

with open(extractedPath, 'w') as extractedFile:
    for extractedToken in extractedTokens:
        extractedFile.write(extractedToken + '\n')