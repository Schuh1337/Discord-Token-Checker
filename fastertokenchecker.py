import os
import time
import ctypes
import asyncio
import aiohttp

GREEN = '\033[92m'
PURPLE = '\033[95m'
RED = '\033[91m'
ENDC = '\033[0m'

validPath = 'valid.txt'
invalidPath = 'invalid.txt'
ctypes.windll.kernel32.SetConsoleTitleW('Token Checker')

def checkDupes(token_list):
    uniqueTokens = set()
    dupeTokens = set()
    uniqueList = []
    for token in token_list:
        token = token.strip()
        if not token:
            continue
        if token not in uniqueTokens:
            uniqueTokens.add(token)
            uniqueList.append(token)
        else:
            dupeTokens.add(token)
    return uniqueList, dupeTokens

async def check(session, email, password, token):
    headers = {'Authorization': token}
    try:
        async with session.get('https://discord.com/api/v10/users/@me', headers=headers) as response:
            if response.status == 200:
                print(GREEN + f'[#] Valid: {token}' + ENDC)
                return True
            else:
                print(RED + f'[#] Invalid: {token}' + ENDC)
                return False
    except Exception as e:
        print(RED + f'[#] Error checking Token: {e}' + ENDC)
        return False

async def main():
    valid = []
    invalid = []
    
    if not os.path.exists(validPath):
        print(RED + f'[!] File {validPath} not found' + ENDC)
        return

    with open(validPath, 'r') as file:
        tokens = file.read().splitlines()
        tokenList = [line.strip() for line in tokens if line.strip()]

    if not tokenList:
        print(RED + f'[!] No tokens found in {validPath}' + ENDC)
        return

    tokenList, dupeTokens = checkDupes(tokenList)
    totalTokens = len([token for token in tokenList if token.strip() and len(token.split(':')) == 3])

    start = time.perf_counter()
    validTokens = 0
    invalidTokens = 0
    processedTokens = 0

    async with aiohttp.ClientSession() as session:
        tasks = []

        for i, token in enumerate(tokenList):
            if not token.strip() or len(token.split(':')) != 3:
                continue
            
            email, password, token = token.split(':')
            tasks.append(check(session, email, password, token))

        results = await asyncio.gather(*tasks)

    for i, (token, result) in enumerate(zip(tokenList, results)):
        if result:
            validTokens += 1
            valid.append(f"{token}")
        else:
            invalidTokens += 1
            invalid.append(f"{token}")

        processedTokens += 1
        ctypes.windll.kernel32.SetConsoleTitleW(f'Token Checker   I   {processedTokens} of {totalTokens} checked   I   {validTokens} Valid   I   {invalidTokens} Invalid   I   {len(dupeTokens)} Duplicate{"s" if int(len(dupeTokens)) != 1 else ""}')

    with open(validPath, 'w') as validFile:
        validFile.write('\n'.join(valid))

    with open(invalidPath, 'a') as invalidFile:
        for invalid_token in invalid:
            invalidFile.write(invalid_token.rstrip() + '\n')

    end = time.perf_counter()
    total = end - start

    print(PURPLE + f'\n[#] {validTokens} Token{"s" if validTokens != 1 else ""} Valid' + ENDC)
    print(PURPLE + f'[#] {invalidTokens} Token{"s"  if invalidTokens != 1 else ""} Invalid' + ENDC)
    minutes, seconds = divmod(total, 60)
    if total <= 60:
        print(PURPLE + f'[#] Took: {total:.2f} second{"s" if seconds != 1 else ""}' + ENDC)
    else:
        print(PURPLE + f'[#] Took: {int(minutes)} minute{"s" if minutes != 1 else ""} {int(seconds)} second{"s" if seconds != 1 else ""}' + ENDC)
    input()

if __name__ == "__main__":
    asyncio.run(main())
