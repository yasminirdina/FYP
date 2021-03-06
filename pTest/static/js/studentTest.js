// Connect with html
const question = document.querySelector('#questionText')
const choices = Array.from(document.querySelectorAll('.choice-text'))
const progressText = document.querySelector('#progressText')
const scoreText = document.querySelector('#score')
const progressBarFull = document.querySelector('#progressBarFull')
const previous = document.querySelector('.prev-text')

// introducing new var
let currentQuestion = {}
let acceptingAnswer = true
let score = 0
let questionCounter = 0
let questionsIndex = 0
let availableQuestions = []
let questions = []
let MAX_QUESTIONS = 0

const SCORE_POINTS = 1
// let questions = [
//     {
//         question: '1 Adakah anda seorang yang Praktikal',
//         choice1: 'Ya',
//         choice2: 'Tidak',
//         answer: 1,
//     },
//     {
//         question: '2 Adakah anda seorang yang Mahir Dalam Sukan Tertentu',
//         choice1: 'Ya',
//         choice2: 'Tidak',
//         answer: 1,
//     },
//     {
//         question: '3 Adakah anda seorang yang Berterus Terang',
//         choice1: 'Ya',
//         choice2: 'Tidak',
//         answer: 1,
//     },
//     {
//         question: '4 Adakah anda seorang yang Cenderung Bidang Mekanikal',
//         choice1: 'Ya',
//         choice2: 'Tidak',
//         answer: 1,
//     },
//     {
//         question: '5 Adakah anda seorang yang Pecinta Alam',
//         choice1: 'Ya',
//         choice2: 'Tidak',
//         answer: 1,
//     },
//     {
//         question: '6 Adakah anda seorang yang Ingin Tahu Tentang Dunia Fizikal',
//         choice1: 'Ya',
//         choice2: 'Tidak',
//         answer: 1,
//     }
// ]

//     MAX_QUESTIONS = 6
//     questionCounter = 0
//     questionsIndex = 0
//     score = 0
//     availableQuestions = [...questions]
//     // calling out each question
//     getNewQuestion()
//     scoreR = score
// }

getNewQuestion = () => {
    // if reached end of question Array, go to result page
    if(availableQuestions.length === 0 || questionCounter > MAX_QUESTIONS) {
        // Store/save the current score in web browser inefinitely
        localStorage.setItem('saveCurrentScore', score)
        return window.location.assign('/endTest.html')
        // return score
    }

    questionCounter++
    // innertext = return text in progress text part in html
    progressText.innerText = `Soalan ${questionCounter} daripada ${MAX_QUESTIONS}`
    // percentage of the progress and style=set the css style in progressbarfull html
    progressBarFull.style.width = `${(questionCounter/MAX_QUESTIONS) * 100}%`

    // currentquest is to keep track the quest we're on
    currentQuestion = availableQuestions[questionsIndex]
    // display the current quest asked
    question.innerText = currentQuestion.question

    // The choices from choice text is an array
    // so for each choice (loop function),
    choices.forEach(choice => {
        // dataset is the data-number in html, save it to number.That way we know what choice we click on
        const number = choice.dataset['number']
        choice.innerText = currentQuestion['choice' + number]
    })
    // splice remove the question in the array and replace it with the next one
    availableQuestions.splice(questionsIndex, 1)
    // questionCounter++
    // questionsIndex++
    acceptingAnswers = true
}

// loop choice
choices.forEach(choice => {
    // addeventlistener = put a click event to the doc so when user clicks on the event akan redirect ke mana yg kita nak
    // e is the event value to be passed when using eventlistener
    choice.addEventListener('click', e => {
        // if there's no choices next or select choice, return
        if(!acceptingAnswers) return

        acceptingAnswers = false
        // target = target/get element where we click on the choice
        const selectedChoice = e.target
        // dataset number is the choice 1,2,3,4
        const selectedAnswer = selectedChoice.dataset['number']

        // if selected answer equals to the current question's answer; 1. if the choice is true, toggle to the css of correct or 2. if the choice is wrong, toggle to the css of incorrect
        let classToApply = selectedAnswer == currentQuestion.answer ? 'correct' : 'incorrect'

        // if user choose correct, increase score
        if (classToApply === 'correct'){
            //call in increment score function
            incrementScore(SCORE_POINTS)
        }

        // add it whenever user got it right
        selectedChoice.parentElement.classList.add(classToApply)

        // give time to show if the answer correct or wrong before moving on to the next question
        setTimeout(()=> {
            selectedChoice.parentElement.classList.remove(classToApply)
            getNewQuestion()
        }, 1000)
    })
})

// calculate score and display updated score in html
incrementScore = num => {
    score += num
    scoreText.innerText = score
}

getQuestR = () => {
    questions = [
        {
            question: 'Adakah anda seorang yang Praktikal',
            choice1: 'Ya',
            choice2: 'Tidak',
            answer: 1,
        },
        {
            question: 'Adakah anda seorang yang Mahir Dalam Sukan Tertentu',
            choice1: 'Ya',
            choice2: 'Tidak',
            answer: 1,
        },
        {
            question: 'Adakah anda seorang yang Berterus Terang',
            choice1: 'Ya',
            choice2: 'Tidak',
            answer: 1,
        },
        {
            question: 'Adakah anda seorang yang Cenderung Bidang Mekanikal',
            choice1: 'Ya',
            choice2: 'Tidak',
            answer: 1,
        },
        {
            question: 'Adakah anda seorang yang Pecinta Alam',
            choice1: 'Ya',
            choice2: 'Tidak',
            answer: 1,
        },
        {
            question: 'Adakah anda seorang yang Ingin Tahu Tentang Dunia Fizikal',
            choice1: 'Ya',
            choice2: 'Tidak',
            answer: 1,
        }
    ]

    MAX_QUESTIONS = 6
    questionCounter = 0
    questionsIndex = 0
    score = 0
    availableQuestions = [...questions]
    getNewQuestion()
    // var scoreR = getNewQuestion()
    // alert(scoreR)
}

getQuestA = () => {
    questions = [
        {
            question: '1 Test',
            choice1: 'Ya',
            choice2: 'Tidak',
            answer: 1,
        },
        {
            question: '2 Test',
            choice1: 'Ya',
            choice2: 'Tidak',
            answer: 1,
        }
    ]

    MAX_QUESTIONS = 2
    questionCounter = 0
    questionsIndex = 0
    score = 0
    availableQuestions = [...questions]
    // calling out each question
    getNewQuestion()
}
// function expression declaration...functionName = (variable) => value
// function to start overall test
startTest = () => {
    getQuestR()
    // questionCounter = 0
    // questionsIndex = 0
    // score = 0
    // availableQuestions = [...questions]
    // // calling out each question
    // getNewQuestion()
}

//-------------------------------------edit-----------------------------------------------
// previous.addEventListener('click', e=> {
    // if(previous.clicked==true){
    // questionCounter--
    // questionsIndex--
    // var choice = confirm(questionCounter)

    // progressText.innerText = `Soalan ${questionCounter} daripada ${MAX_QUESTIONS}`
    // progressBarFull.style.width = `${(questionCounter/MAX_QUESTIONS) * 100}%`
    
    // let tempIndex = questionsIndex--
    // questionsIndex = tempIndex
    // currentQuestion = availableQuestions[questionsIndex]
    // question.innerText = currentQuestion.question

    // choices.forEach(choice => {
    //     const number = choice.dataset['number']
    //     choice.innerText = currentQuestion['choice' + number]
    // })

    // getNewQuestion()
// })


startTest()