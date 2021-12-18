var user_id = '{{ user_id }}';
var cnt_quest = parseInt(document.querySelector('.cnt_quest').innerText);
var next_cnt_ques = parseInt(document.querySelector('.p-next_cnt_ques').innerText);
var hasSubmitted = document.querySelector('.p-hasSubmitted').innerText;
var isCorrect = document.querySelector('.p-isCorrect').innerText;
var i = 0;
var k = 0;
var m = 0;
var bar_ques = document.querySelector('.div-bar-timer-ques');
var width_ques = 0;
var id_ques = 0;
var timeLimit = parseInt(document.querySelector('.p-timeLimit').innerText);
var clickedQuit = false;
var clickedHint = false;
var clickedHint2 = false;
var doneViewHint = false;

$('#progressBarFull').width((cnt_ques/10) * 100 + "%");

function setCookie(c_name,value,exdays) {
    if (c_name == 'mainMuted') {
        var exdate=new Date();
        exdate.setDate(exdate.getDate() + exdays);
        var c_value = escape(value) + ((exdays==null) ? "" : "; expires="+exdate.toUTCString()) + "; path=/";
        document.cookie=c_name + "=" + c_value;
    }
}

function getCookie(c_name) {
    var i,x,y,ARRcookies=document.cookie.split(";");
    for (i=0;i<ARRcookies.length;i++) {
        x=ARRcookies[i].substr(0,ARRcookies[i].indexOf("="));
        y=ARRcookies[i].substr(ARRcookies[i].indexOf("=")+1);
        x=x.replace(/^\s+|\s+$/g,"");
        if (x==c_name) {
            return unescape(y);
        }
    }
}

var audio  = new Audio('/static/audio/clickDown.mp3');
var audio2 = new Audio('/static/audio/clickUp.mp3');
var audio3  = new Audio('/static/audio/correctAnswer.wav');
var audio4 = new Audio('/static/audio/wrongAnswer.wav');
var audio5 = new Audio('/static/audio/showHint.wav');
audio.volume = 0.5;
audio2.volume = 0.5;
audio3.volume = 0.5;
audio4.volume = 0.5;
audio5.volume = 0.5;

var song = document.getElementsByTagName('audio')[0];
var isSongMuted = getCookie('mainMuted');
const musicBtn = document.getElementById('music-play')
const musicIcon = document.getElementsByClassName('fas')
song.volume = 0.5;
song.play();

$(document).ready(function() {
    if (isSongMuted) {
        if (isSongMuted == 'false') {
            song.muted = false;
            $('#music-icon').removeClass('fas');
            $('#music-icon').addClass('fas fa-volume-up');
        }
        else if (isSongMuted == 'true') {
            song.muted = true;
            $('#music-icon').removeClass('fas');
            $('#music-icon').addClass('fas fa-volume-mute');
        }
    }
    else {
        song.muted = false;
        $('#music-icon').removeClass('fas');
        $('#music-icon').addClass('fas fa-volume-up');
    }
});

musicBtn.addEventListener('click', () => {
    audio2.play();
    audio.play();
    if (song.muted == false) {
        song.muted = true;
        $('#music-icon').removeClass('fas fa-volume-up');
        $('#music-icon').addClass('fas fa-volume-mute');
    }
    else if (song.muted == true) {
        song.muted = false;
        $('#music-icon').removeClass('fas fa-volume-mute');
        $('#music-icon').addClass('fas fa-volume-up');
    }
});

setInterval(setCookie('mainMuted', song.muted), 1000); //0 for localhost & testing only

function submit_form() {
    // alert("(isClicked=" + $('#isClicked').val() + ") Enter form submit");
    $.ajax({
        headers: { "X-CSRFToken": '{{csrf_token}}' }, 
        url: "{% url 'quiz:quiz-play' user_id field_id %}",
        data: {
            isClicked: $('#isClicked').val(),
            answer_choices: $('input[name=answer_choices]:checked').val(),
            cnt_ques: cnt_ques
        },
        type: 'POST',
        success: function(result){
            // alert("(isClicked=" + $('#isClicked').val() + ") Succeed submit form");
            $("#div-wrapper").html(result);
            $('#progressBarFull').width((cnt_ques/10) * 100 + "%");
            hasSubmitted = document.querySelector('.p-hasSubmitted').innerText;
            isCorrect = document.querySelector('.p-isCorrect').innerText;
            var currPlayerAllFieldScoreText = document.querySelector('.span-value-totalScore'); //in player navbar
            currPlayerAllFieldScoreText.innerText = document.querySelector('.p-totalPoints_2').innerText;

            if (hasSubmitted == 'True') {
                if (isCorrect == 'True') {
                    audio3.load();
                    audio3.play();
                    currPlayerAllFieldScoreText.className = "span-value-totalScore correct";
                }
                else {
                    audio4.load();
                    audio4.play();
                }
            }
        },
        error: function(result){
            // alert("(isClicked=" + $('#isClicked').val() + ") Failed submit form");
        }
    });
}

function update_frameques() {
    if (hasSubmitted == 'False') {
        if (m == 0) {
            m = 1;
            id_ques = setInterval(frame_ques, 1000);
        }
    }
}

function frame_ques() {
    if (width_ques >= 100) {
        clearInterval(id_ques);
        m = 0;
        submit_form();
    } else {
        $(".choice-text").on('click', function() {
            audio2.play();
            audio.play();
        });

        if (clickedHint == true) {
            modal2 = document.querySelector('.div-bg-modal2');
            modal2.style.display = "flex";
            clearInterval(id_ques);
        }
        else if (clickedQuit == true) {
            modal1 = document.querySelector('.div-bg-modal');
            modal1.style.display = "flex";
            clearInterval(id_ques);
        }
        else {
            if (timeLimit == 10){
                width_ques += 10;
            }
            else if (timeLimit == 20){
                width_ques += 5;
            }
            else {
                width_ques += 3.33;
            }
            bar_ques.style.width = width_ques + "%";
        }
    }
}

update_frameques();

$('#div-wrapper').on('click', '.next', function(){
    audio2.play();
    audio.play();
    clearInterval(id_ques);
    // alert("hi next clicked");
    var endWidth = bar_ques.style.width.slice(0, -1);
    var currPlayerAllFieldScoreText = document.querySelector('.span-value-totalScore'); //in player navbar TEST
    // alert(endWidth + ", type: " + typeof endWidth + ", currTotalScore: " + currPlayerAllFieldScoreText.innerText);
    $.ajax({
        headers: { "X-CSRFToken": '{{csrf_token}}' }, 
        url: "{% url 'quiz:quiz-play' user_id field_id %}",
        data: {
            'endWidth': endWidth,
            'timeLimit': timeLimit,
            'requestType': 'Next'
        },
        type: 'POST',
        dataType: 'json',
        success: function(result){
            document.getElementById('isClicked').value = result.isClicked
            // alert("Succeed update isClicked");
            submit_form();
        },
        error: function(result){
            // alert("Failed update isClicked");
        }
    })
});

$('#div-wrapper').on('click', '.next2', function(){
    audio2.play();
    audio.play();
    next_cnt_ques = parseInt(document.querySelector('.p-next_cnt_ques').innerText);
    // alert("next_cnt_ques: " + next_cnt_ques.toString());
    $.ajax({
        url: "{% url 'quiz:quiz-play' user_id field_id %}",
        data: {
            'cnt_ques': next_cnt_ques,
        },
        type: 'GET',
        success: function(result){
            // alert("Succeed go to next question");
            $("#div-wrapper").html(result);
            var currPlayerAllFieldScoreText = document.querySelector('.span-value-totalScore'); //in player navbar
            currPlayerAllFieldScoreText.innerText = document.querySelector('.p-totalPoints_2').innerText;
            if (currPlayerAllFieldScoreText.className == "span-value-totalScore correct"){
                currPlayerAllFieldScoreText.className = "span-value-totalScore";
            }
            cnt_ques = parseInt(document.querySelector('.p-cnt_ques').innerText)
            $('#progressBarFull').width((cnt_ques/10) * 100 + "%");
            hasSubmitted = document.querySelector('.p-hasSubmitted').innerText;
            i = 0;
            k = 0;
            m = 0;
            bar_ques = document.querySelector(".div-bar-timer-ques");
            width_ques = 0;
            id_ques = 0;
            timeLimit = parseInt(document.querySelector('.p-timeLimit').innerText);
            clickedQuit = false;
            clickedHint = false;
            clickedHint2 = false;
            doneViewHint = false;
            update_frameques();
        },
        error: function(result){
            // alert("Fail go to next question");
        }
    })
});

$('#div-wrapper').on('click', '.quit', function(){
    audio2.play();
    audio.play();
    clickedQuit = true;
    hasSubmitted = document.querySelector('.p-hasSubmitted').innerText;
    if (hasSubmitted == 'True'){
        modal1 = document.querySelector('.div-bg-modal');
        modal1.style.display = "flex";
    }
});

$('#div-wrapper').on('click', '.quit-for-quizPlay', function(){
    audio2.play();
    audio.play();
    window.location.href = "/kuiz/pelajar/" + user_id + "/";
})

$('#div-wrapper').on('click', '.cancelQuit-for-quizPlay', function(){
    audio2.play();
    audio.play();
    modal1.style.display = "none";
    clickedQuit = false;
    if (hasSubmitted == 'False'){
        id_ques = setInterval(frame_ques, 1000);
        update_frameques();
    }
})

$('#div-wrapper').on('click', '.showResult', function(){
    audio2.play();
    audio.play();
    // alert("hi");
    $.ajax({
        headers: { "X-CSRFToken": '{{csrf_token}}' }, 
        url: "{% url 'quiz:quiz-play' user_id field_id %}",
        data: {
            'requestType': 'updateStatusSessionRecord'
        },
        type: 'POST',
        success: function(response){
            // alert("updateStatusSessionRecord: success");
            window.location.href = "{% url 'quiz:quiz-result' user_id field_id %}";
        },
        error: function(response){
            // alert("updateStatusSessionRecord: success");
        }
    })
});

$('#div-wrapper').on('click', '.hint', function(){
    audio2.play();
    audio.play();
    clickedHint = true;
});

$('#div-wrapper').on('click', '.useHint-for-quizPlay', function(){
    audio2.play();
    audio.play();
    clickedHint2 = true;

    var bar_hint = document.querySelector('.div-bar-timer-hint');
    // alert(bar_hint.getAttribute("class")); //test
    var width_hint = 0;
    var id_hint = 0;

    modal2.style.display = "none";
    modal3 = document.querySelector('.div-bg-modal3');
    modal3.style.display = "flex";
    audio5.play();
    if (i == 0) {
        i = 1;
        id_hint = setInterval(frame_hint, 1000);

        function frame_hint() {
            if (width_hint >= 100) {
                clearInterval(id_hint);
                i = 0;
                modal3.style.display = "none";
                clickedHint = false;
                clickedHint2 = false;
                doneViewHint = true;

                update_hint();

                id_ques = setInterval(frame_ques, 1000);
                update_frameques();
            } else {
                width_hint += 10;
                bar_hint.style.width = width_hint + "%";
            }
        }
    }
});

$('#div-wrapper').on('click', '.cancelHint1-for-quizPlay', function(){
    audio2.play();
    audio.play();
    modal2.style.display = "none";
    clickedHint = false;
    id_ques = setInterval(frame_ques, 1000);
    update_frameques();
});

$('#div-wrapper').on('click', '.cancelHint2-for-quizPlay', function(){
    audio2.play();
    audio.play();
    modal2.style.display = "none";
    clickedHint = false;
    id_ques = setInterval(frame_ques, 1000);
    update_frameques();
});

function update_hint() {
    var cntHint = parseInt(document.querySelector('.p-cntHint').innerText) - 1;
    var currentHintID = parseInt(document.querySelector('.p-randomHintID').innerText);

    // HINT 1
    $.ajax({
        headers: { "X-CSRFToken": '{{csrf_token}}' }, 
        url: "{% url 'quiz:quiz-play' user_id field_id %}",
        data: {
            'cntHint': cntHint,
            'usedHintID': currentHintID,
            'requestType': 'updateBalanceHint_1'
        },
        type: 'POST',
        success: function(result){
            // alert('updateBalanceHint_1: cntHint updated');
            $("#hint-wrapper").html(result);
            //take the hidden points and total points values from updateBalanceHint1.html to replace the values displayed
            //in top navbar and header
            var currPlayerAllFieldScoreText = document.querySelector('.span-value-totalScore'); //in player navbar
            var currentSessionScore = document.querySelector('.score'); //in header
            currPlayerAllFieldScoreText.innerText = document.querySelector('.p-totalPoints').innerText;
            currentSessionScore.innerText = document.querySelector('.p-points').innerText;

            // HINT 2
            $.ajax({
                headers: { "X-CSRFToken": '{{csrf_token}}' }, 
                url: "{% url 'quiz:quiz-play' user_id field_id %}",
                data: {
                    'cntHint': cntHint,
                    'requestType': 'updateBalanceHint_2'
                },
                type: 'POST',
                success: function(result){
                    // alert('updateBalanceHint_2: cntHint updated');
                    $("#hint-button-wrapper").html(result);

                    // HINT 3
                    $.ajax({
                        headers: { "X-CSRFToken": '{{csrf_token}}' }, 
                        url: "{% url 'quiz:quiz-play' user_id field_id %}",
                        data: {
                            'cntHint': cntHint,
                            'usedHintID': currentHintID,
                            'requestType': 'updateHint_3'
                        },
                        type: 'POST',
                        success: function(result){
                            // alert('updateHint_3: cntHint, randomHint, currentFieldPlayerSession updated');
                            $("#modal2-wrapper").html(result);

                            // HINT 4
                            $.ajax({
                                headers: { "X-CSRFToken": '{{csrf_token}}' }, 
                                url: "{% url 'quiz:quiz-play' user_id field_id %}",
                                data: {
                                    'cntHint': cntHint,
                                    'usedHintID': currentHintID,
                                    'requestType': 'updateHint_4'
                                },
                                type: 'POST',
                                success: function(result){
                                    // alert('updateHint_4: cntHint, randomHint updated');
                                    $("#modal3-wrapper").html(result);
                                },
                                error: function(response){
                                    // alert("updateHint_4: cntHint, randomHint NOT updated");
                                }
                            })
                        },
                        error: function(response){
                            // alert("updateHint_3: cntHint, randomHint,currentFieldPlayerSession NOT updated");
                        }
                    })
                },
                error: function(response){
                    // alert("updateBalanceHint_2: cntHint NOT updated");
                }
            })
        },
        error: function(response){
            // alert("updateBalanceHint_1: cntHint NOT updated");
        }
    })
}