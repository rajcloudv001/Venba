from flask import Flask, render_template, request, jsonify


app = Flask(__name__, static_url_path='')

def process(input):
    SIGN_ANUSVARA  = '0b82'    # 'ஂ '
    SIGN_VISARGA   = '0b83'    # 'ஃ '
    LETTER_A       = '0b85'    # 'அ '
    LETTER_AA      = '0b86'    # 'ஆ '
    LETTER_I       = '0b87'    # 'இ '
    LETTER_II      = '0b88'    # 'ஈ '
    LETTER_U       = '0b89'    # 'உ '
    LETTER_UU      = '0b8a'    # 'ஊ'
    LETTER_E       = '0b8e'    # 'எ '
    LETTER_EE      = '0b8f'    # 'ஏ '
    LETTER_AI      = '0b90'    # 'ஐ '
    LETTER_O       = '0b92'    # 'ஒ '
    LETTER_OO      = '0b93'    # 'ஓ '
    LETTER_AU      = '0b94'    # 'ஔ'
    LETTER_KA      = '0b95'    # 'க '
    LETTER_NGA     = '0b99'    # 'ங '
    LETTER_CA      = '0b9a'    # 'ச '
    LETTER_JA      = '0b9c'    # 'ஜ '
    LETTER_NYA     = '0b9e'    # 'ஞ '
    LETTER_TTA     = '0b9f'    # 'ட '
    LETTER_NNA     = '0ba3'    # 'ண'
    LETTER_TA      = '0ba4'    # 'த '
    LETTER_NA      = '0ba8'    # 'ந '
    LETTER_NNNA    = '0ba9'    # 'ன '
    LETTER_PA      = '0baa'    # 'ப '
    LETTER_MA      = '0bae'    # 'ம '
    LETTER_YA      = '0baf'    # 'ய '
    LETTER_RA      = '0bb0'    # 'ர '
    LETTER_RRA     = '0bb1'    # 'ற '
    LETTER_LA      = '0bb2'    # 'ல '
    LETTER_LLA     = '0bb3'    # 'ள '
    LETTER_LLLA    = '0bb4'    # 'ழ '
    LETTER_VA      = '0bb5'    # 'வ '
    LETTER_SHA     = '0bb6'    # 'ஶ'
    LETTER_SSA     = '0bb7'    # 'ஷ'
    LETTER_SA      = '0bb8'    # 'ஸ '
    LETTER_HA      = '0bb9'    # 'ஹ'
    VOWEL_SIGN_AA  = '0bbe'    # 'ா '
    VOWEL_SIGN_I   = '0bbf'    # 'ி '
    VOWEL_SIGN_II  = '0bc0'    # 'ீ '
    VOWEL_SIGN_U   = '0bc1'    # 'ு '
    VOWEL_SIGN_UU  = '0bc2'    # 'ூ'
    VOWEL_SIGN_E   = '0bc6'    # 'ெ'
    VOWEL_SIGN_EE  = '0bc7'    # 'ே '
    VOWEL_SIGN_AI  = '0bc8'    # 'ை'
    VOWEL_SIGN_O   = '0bca'    # 'ொ'
    VOWEL_SIGN_OO  = '0bcb'    # 'ோ'
    VOWEL_SIGN_AU  = '0bcc'    # 'ௌ'
    SIGN_VIRAMA    = '0bcd'    # '் '
    AU_LENGTH_MARK = '0bd7'    # 'ௗ'



    UYIR_KURIL = [LETTER_A, LETTER_I, LETTER_U, LETTER_E, LETTER_O]
    MEI_KURIL = [ LETTER_KA, LETTER_NGA,
                 LETTER_CA, LETTER_JA, LETTER_NYA, LETTER_TTA, LETTER_NNA, LETTER_TA,
                 LETTER_NA, LETTER_NNNA, LETTER_PA, LETTER_MA, LETTER_YA, LETTER_RA,
                 LETTER_RRA, LETTER_LA, LETTER_LLA, LETTER_LLLA, LETTER_VA, LETTER_SHA,
                 LETTER_SSA, LETTER_SA, LETTER_HA]

    OTRU = [SIGN_ANUSVARA, SIGN_VIRAMA]

    LUGARAM = [ VOWEL_SIGN_U ]

    AAYUTHAM = [SIGN_VISARGA]

    UYIR_NEDIL = [ LETTER_AA, LETTER_II, LETTER_UU, LETTER_EE, LETTER_AI, LETTER_OO, LETTER_AU ]

    VOWEL_NEDIL = [ VOWEL_SIGN_AA, VOWEL_SIGN_II, VOWEL_SIGN_UU, VOWEL_SIGN_EE, VOWEL_SIGN_AI,
                   VOWEL_SIGN_OO, VOWEL_SIGN_AU, AU_LENGTH_MARK ]

    VOWEL_KURIL = [VOWEL_SIGN_I, VOWEL_SIGN_U, VOWEL_SIGN_E, VOWEL_SIGN_O]

    ALLCHAR = UYIR_KURIL + MEI_KURIL + OTRU + LUGARAM + AAYUTHAM + UYIR_NEDIL + VOWEL_NEDIL + VOWEL_KURIL

    NER = 'நேர்/'
    NIRAI = 'நிரை/'
    NERBU = 'நேர்பு/'
    NIRAIBU = 'நிரைபு/'

    NAAL = "நாள்"
    MALAR = "மலர்"
    KAASU = "காசு"
    PIRAPPU = "பிறப்பு"

    invalid = '**தவறான சீர்**'
    successMessage = 'சீர் அசை சரியாக அமைந்துள்ள குறள் வெண்பா'
    failureMessage = 'அசை தவறாக உள்ளது.  அசை திருத்தி மீண்டும் சரிபார்க்கவும்'
    eetruSeerMessage = 'ஈற்றடி ஈற்றுச் சீர் ஓரசைச் சீர் வரவேண்டும். திருத்தி மீண்டும் சரிபார்க்கவும்'
    yeluSeerIssueMessage = 'முதலடி நான்கு சீர்கள், இரண்டாம் அடி மூன்று சீர்கள் கொண்டதாக இருக்க வேண்டும்'
    kanichcheerErrorMEssage = 'கனிச்சீர் வரக்கூடாது. திருத்தி மீண்டும் சரிபார்க்கவும்'
    niraiNiraiErrorMessage = '***/***/நேர் நேர்/***[/***] என்று அமைய வேண்டும். திருத்தி மீண்டும் சரிபார்க்கவும்'
    nerNiraiErrorMessage = '***/நேர் நிரை/***[/***] என்று அமைய வேண்டும். திருத்தி மீண்டும் சரிபார்க்கவும்'
    niraiNErErrorMessage = '***/நிரை நேர்/***[/***] என்று அமைய வேண்டும். திருத்தி மீண்டும் சரிபார்க்கவும்'
    nerEettruErrorMessage = 'ஈற்றுச்சீர் [***/]***/நேர் நிரை (அ) நிரைபு என்று அமைய வேண்டும். திருத்தி மீண்டும் சரிபார்க்கவும்'
    niraiEetruErrorMessage = 'ஈற்றுச்சீர் [***/]***/நிரை நேர் (அ) நேர்பு என்று அமைய வேண்டும். திருத்தி மீண்டும் சரிபார்க்கவும்'



    EETRUSEER = [NAAL, MALAR, KAASU, PIRAPPU]

    seer = {
    NER : NAAL,
    NIRAI : MALAR,
    NERBU : KAASU,
    NIRAIBU : PIRAPPU,
    NER + NER : "தேமா",
    NER + NIRAI : "கூவிளம்",
    NIRAI + NER : "புளிமா",
    NIRAI + NIRAI : "கருவிளம்",
    NER + NER + NER : "தேமாங்காய்",
    NER + NIRAI + NER : "கூவிளங்காய்",
    NIRAI + NER + NER : "புளிமாங்காய்",
    NIRAI + NIRAI + NER : "கருவிளங்காய்",
    NER + NER + NIRAI : "தேமாங்கனி",
    NIRAI + NER + NIRAI : "புளிமாங்கனி",
    NER + NIRAI + NIRAI : "கூவிளங்கனி",
    NIRAI + NIRAI + NIRAI : "கருவிளங்கனி",
    NER + NER + NER + NER : "தேமாந்தண்பூ",
    NER + NER + NER + NIRAI : "தேமாந்தண்ணிழல்",
    NER + NER + NIRAI + NER : "தேமாநறும்பூ",
    NER + NER + NIRAI + NIRAI : "தேமாநறுநிழல்",
    NER + NIRAI + NER + NER : "கூவிளந்தண்பூ",
    NER + NIRAI + NER + NIRAI : "கூவிளந்தண்ணிழல்",
    NER + NIRAI + NIRAI + NER : "கூவிளநறும்பூ",
    NER + NIRAI + NIRAI + NIRAI : "கூவிளநறுநிழல்",
    NIRAI + NIRAI + NER + NER : "கருவிளந்தண்பூ",
    NIRAI + NIRAI + NER + NIRAI : "கருவிளந்தண்ணிழல்",
    NIRAI + NIRAI + NIRAI + NER : "கருவிளநறும்பூ",
    NIRAI + NIRAI + NIRAI + NIRAI : "கருவிளநறுநிழல்",
    NIRAI + NER + NER + NER : "புளிமாந்தண்பூ",
    NIRAI + NER + NER + NIRAI : "புளிமாந்தண்ணிழல்",
    NIRAI + NER + NIRAI + NER : "புளிமாநறும்பூ",
    NIRAI + NER + NIRAI + NIRAI : "புளிமாநறுநிழல்"}

    VENBASEER = ["தேமா", "கூவிளம்", "புளிமா", "கருவிளம்", "தேமாங்காய்", "கூவிளங்காய்", "புளிமாங்காய்", "கருவிளங்காய்"] + EETRUSEER

    message = ''

    newlineByte = "b'\\\\n'"
    spaceByte = "b' '"
    SPACE = " "
    NEWLINE = "\n"
    unicode = []
    for char in input:
        uChar = str(char.encode("unicode_escape"))
        if uChar == spaceByte:
            unicode.append(SPACE)
        elif uChar == newlineByte:
            unicode.append(NEWLINE)
        else:
            if uChar[-5:-1] in ALLCHAR:
                unicode.append(uChar[-5:-1])

        i = 0
        wordScore = []
        inputWithSeer = []
        j = 0
        maxIdx = len(unicode)
        while i < maxIdx:
            if len(unicode[i]) < 4:
                wordScore.append(unicode[i])
                inputWithSeer.append(unicode[i])
            else:
                if unicode[i] in UYIR_KURIL:
                    wordScore.append('2')
                    inputWithSeer.append(unicode[i])
                elif unicode[i] in AAYUTHAM:
                    wordScore.append('1')
                    inputWithSeer.append(unicode[i])
                elif unicode[i] in MEI_KURIL:
                    if i + 1 < maxIdx:
                        if unicode[i + 1] in UYIR_KURIL + UYIR_NEDIL + MEI_KURIL + [SPACE, NEWLINE] + AAYUTHAM:
                            wordScore.append('2')
                            inputWithSeer.append(unicode[i])
                        else:
                            inputWithSeer.append(unicode[i])
                            if unicode[i + 1] in VOWEL_NEDIL:
                                wordScore.append('4')
                                inputWithSeer.append(unicode[i + 1])
                                i += 1
                            elif unicode[i + 1] in VOWEL_KURIL:
                                wordScore.append('2')
                                inputWithSeer.append(unicode[i + 1])
                                i += 1
                            elif unicode[i + 1] in OTRU:
                                wordScore.append('1')
                                inputWithSeer.append(unicode[i + 1])
                                i += 1
                    else:
                        wordScore.append('2')
                        inputWithSeer.append(unicode[i])
                elif unicode[i] in UYIR_NEDIL:
                    wordScore.append('4')
                    inputWithSeer.append(unicode[i])
            if len(wordScore) >= 1:
                if wordScore[-1] == '1':
                    inputWithSeer.append('/')
                elif wordScore[-1] == '4':
                    if len(wordScore) >= 2:
                        if wordScore[-2] in ['4']:
                            if inputWithSeer[-1] in VOWEL_NEDIL + VOWEL_KURIL:
                                inputWithSeer.insert(-2, '/')
                            elif inputWithSeer[-1] in UYIR_NEDIL:
                                inputWithSeer.insert(-1, '/')
                        elif wordScore[-2] in ['2']:
                            if inputWithSeer[-1] in UYIR_NEDIL:
                                inputWithSeer.insert(-1, '/')
                            elif len(wordScore) >= 3:
                                if wordScore[-3] == '2':

                                    if inputWithSeer[-1] in VOWEL_KURIL + VOWEL_NEDIL:
                                        if inputWithSeer[-3] in MEI_KURIL and inputWithSeer[-4] in MEI_KURIL:
                                            inputWithSeer.insert(-2, '/')
                                    elif inputWithSeer[-1] in MEI_KURIL:
                                        inputWithSeer.insert(-1, '/')
                                    elif inputWithSeer[-2] in VOWEL_NEDIL + VOWEL_KURIL + UYIR_NEDIL:
                                        inputWithSeer.insert(-1, '/')
                                else:
                                    if inputWithSeer[-1] in UYIR_NEDIL:
                                        inputWithSeer.insert(-1, '/')

                elif wordScore[-1] == '2':
                    if len(wordScore) >= 2:
                        if wordScore[-2] in ['4']:
                            if inputWithSeer[-1] in VOWEL_KURIL:
                                inputWithSeer.insert(-2, '/')
                            elif inputWithSeer[-1] in MEI_KURIL:
                                inputWithSeer.insert(-1, '/')
                            elif inputWithSeer[-2] in VOWEL_NEDIL + VOWEL_KURIL + UYIR_NEDIL:
                                inputWithSeer.insert(-1, '/')
                        elif wordScore[-2] in ['2']:
                            if inputWithSeer[-1] in UYIR_NEDIL:
                                inputWithSeer.insert(-2, '/')
                            elif len(wordScore) >= 3:
                                if wordScore[-3] == '2':
                                    if inputWithSeer[-1] in VOWEL_KURIL:
                                        inputWithSeer.insert(-2, '/')
                                    elif inputWithSeer[-3] in UYIR_KURIL + MEI_KURIL + VOWEL_KURIL:
                                        inputWithSeer.insert(-1, '/')

            i += 1
    inputWithSeerRefined = []
    for i in inputWithSeer:
        if len(i) < 4:
            inputWithSeerRefined.append(i)
        else:
            inputWithSeerRefined.append(('\\u' + i).encode().decode("unicode_escape"))
    inputWithSeerRefined = ''.join(inputWithSeerRefined)

    if maxIdx > 3:
        if unicode[-1] in LUGARAM:
            if unicode[-3] != SPACE:
                wordScore[-1] = '0'

    tempWordScore = ''.join([x.replace(NEWLINE, SPACE + NEWLINE + SPACE) for x in wordScore])
    wordScoreForSeer = [list(i) for i in tempWordScore.split(' ')]
    seerOutput = []
    j = 0
    delimit = ' '
    for word in wordScoreForSeer:
        wordLen = len(word)
        i = 0
        while i < wordLen:
            if word[i] == '1' and i == 0:
                seerOutput.append('-1')
            elif word[i] == '0':
                if seerOutput[-1] == NER:
                    seerOutput[-1] = NERBU
                elif seerOutput[-1] == NIRAI:
                    seerOutput[-1] = NIRAIBU
                elif seerOutput[-1] == delimit:
                    seerOutput.append(NER)
            elif word[i] == NEWLINE:
                seerOutput.append(NEWLINE)
            else:
                if i + 1 < wordLen:
                    if word[i + 1] == '1':
                        seerOutput.append(NER)
                        i += 1
                    elif word[i] == '4':
                        seerOutput.append(NER)
                        if i + 1 < wordLen:
                            if word[i + 1] == '1':
                                i += 1
                    elif word[i] == '2':
                        if word[i + 1] == '4':
                            seerOutput.append(NIRAI)
                            if i + 2 < wordLen:
                                if word[i + 2] == '1':
                                    i += 1
                            i += 1
                        elif word[i + 1] == '2':
                            seerOutput.append(NIRAI)
                            if i + 2 < wordLen:
                                if word[i + 2] == '1':
                                    i += 1
                            i += 1
                else:
                    if word[i] in ['2', '4']:
                        seerOutput.append(NER)
            i += 1
        seerOutput.append(delimit)
    seerOutputSend = (''.join(seerOutput)).replace('\n ', '\n')
    seerOutputString = ''.join(seerOutput)
    seerOutputString = seerOutputString.strip()
    seerOutputList = seerOutputString.split(delimit)

    asai = []
    for i in seerOutputList:
        if i in seer.keys():
            asai.append(seer[i])
        elif i == '\n':
            asai.append('\n')
        elif i in [' ', '']:
            pass
        else:
            asai.append(invalid)
    # print((' '.join(fn3)).replace('\n ','\n'), end = '\n\n')

    tempSeerOutputString = (seerOutputString.replace('\n', ' ').replace('  ', ' ').replace('  ', ' ')).strip()

    if invalid in asai:
        message = failureMessage
    elif tempSeerOutputString.count(' ') + 1 != 7:
        message = yeluSeerIssueMessage
    elif asai[-1] not in EETRUSEER:
        message = eetruSeerMessage
    else:
        sFlag = True
        for i in asai:
            if i not in ['', ' ', '\n']:
                if i not in VENBASEER:
                    print(', '.join(VENBASEER) + ' இவை மட்டுமே ஏற்புடையவை. திருத்தி மீண்டும் சரிபார்க்கவும்')
                    sFlag = False
                    break
        if sFlag:
            tempSeerOutputString = (seerOutputString.replace('\n', '').replace('  ', ' ')).split(' ')
            lenFn4 = len(tempSeerOutputString)
            i = 0
            while i < lenFn4 - 2:
                curLst = tempSeerOutputString[i].strip('/').split('/')
                nxtLst = tempSeerOutputString[i + 1].strip('/').split('/')
                if len(curLst) == 3 and curLst[-1] == NER.strip('/') and nxtLst[0] != NER.strip('/'):
                    message = niraiNiraiErrorMessage
                    sFlag = False
                    break
                elif len(curLst) == 2 and curLst[-1] == NER.strip('/') and nxtLst[0] != NIRAI.strip('/'):
                    message = nerNiraiErrorMessage
                    sFlag = False
                    break
                elif len(curLst) == 2 and curLst[-1] == NIRAI.strip('/') and nxtLst[0] != NER.strip('/'):
                    message = niraiNErErrorMessage
                    sFlag = False
                    break 
                i += 1
        if sFlag:
            curLst = tempSeerOutputString[-1].strip('/').split('/')
            prevLst = tempSeerOutputString[-2].strip('/').split('/')
            if prevLst[-1] == NIRAI.strip('/') and curLst[0] not in [NER.strip('/'), NERBU.strip('/')]:
                message = niraiEetruErrorMessage
                sFlag = False
            elif prevLst[-1] == NER.strip('/') and curLst[0] not in [NIRAIBU.strip('/'), NIRAIBU.strip('/')]:
                message = nerEettruErrorMessage
                sFlag = False

        if sFlag:
            message = successMessage
    output = input + '\n\n' + inputWithSeerRefined + '\n\n' + seerOutputSend + '\n\n' + message
    return output


#@app.route('/')
#def render_main():
#    return render_template("index.html")


@app.route('/process', methods=['POST'])
def startProcess():
	output = ''
	if request.method == 'POST':
		input = request.form['input']
		try:
			output = process(input)
		except Exception:
			output = ''
	
	return output

if __name__ == '__main__':
    app.run() #host='0.0.0.0', port='8000', debug=True)

