var user_id = '{{ user_id }}';
var cnt_quest = parseInt(document.querySelector('.cnt_quest').innerText);
var next_cnt_quest = parseInt(document.querySelector('.next_cnt_quest').innerText);
var hasSubmitted = document.querySelector('.hasSubmitted').innerText;
var isCorrect = document.querySelector('.isCorrect').innerText;
var i = 0;
var k = 0;
var m = 0;
var bar_quest = document.querySelector('.div-bar-timer-quest');
var width_quest = 0;
var id_quest = 0;
var clickedQuit = false;
// var timeLimit = parseInt(document.querySelector('.p-timeLimit').innerText);

//changing the bar width
$('#progressBarFull').width((cnt_quest/10) * 100 + "%");
// document.querySelector('#progressBarFull').style.width = `${(cnt_quest/10) * 100}%`; 

// function setCookie(c_name,value,exdays) {
//     if (c_name == 'mainMuted') {
//         var exdate=new Date();
//         exdate.setDate(exdate.getDate() + exdays);
//         var c_value = escape(value) + ((exdays==null) ? "" : "; expires="+exdate.toUTCString()) + "; path=/";
//         document.cookie=c_name + "=" + c_value;
//     }
// }

// function getCookie(c_name) {
//     var i,x,y,ARRcookies=document.cookie.split(";");
//     for (i=0;i<ARRcookies.length;i++) {
//         x=ARRcookies[i].substr(0,ARRcookies[i].indexOf("="));
//         y=ARRcookies[i].substr(ARRcookies[i].indexOf("=")+1);
//         x=x.replace(/^\s+|\s+$/g,"");
//         if (x==c_name) {
//             return unescape(y);
//         }
//     }
// }

// setInterval(setCookie('mainMuted', song.muted), 1000); //0 for localhost & testing only

// operation once form is submitted
function submit_form() {
    // alert("(isClicked=" + $('#isClicked').val() + ") Enter form submit");
    $.ajax({
        headers: { "X-CSRFToken": '{{csrf_token}}' }, 
        url: "{% url 'test:test-student' user_type user_id %}",
        data: {
            isClicked: $('#isClicked').val(),
            answer_choices: $('input[name=answer_choices]:checked').val(),
            cnt_quest: cnt_quest
        },
        type: 'POST',
        success: function(result){
            // alert("(isClicked=" + $('#isClicked').val() + ") Succeed submit form");
            $("#div-wrapper").html(result);
            $('#progressBarFull').width((cnt_quest/10) * 100 + "%");
            hasSubmitted = document.querySelector('.hasSubmitted').innerText;
            isCorrect = document.querySelector('.isCorrect').innerText;
            // var currPlayerAllFieldScoreText = document.querySelector('.span-value-totalScore'); //in player navbar
            // currPlayerAllFieldScoreText.innerText = document.querySelector('.p-totalPoints_2').innerText;

            // if (hasSubmitted == 'True') {
            //     if (isCorrect == 'True') {
            //         currPlayerAllFieldScoreText.className = "span-value-totalScore correct";
            //     }
            //     else {
            //         audio4.load();
            //         audio4.play();
            //     }
            // }
        },
        error: function(result){
            // alert("(isClicked=" + $('#isClicked').val() + ") Failed submit form");
        }
    });
}

// update question display
function update_framequest() {
    if (hasSubmitted == 'False') {
        if (m == 0) {
            m = 1;
            id_quest = setInterval(frame_quest, 1000);
        }
    }
}

//display quest function
function frame_quest() {
    if (width_quest >= 100) {
        clearInterval(id_quest);
        m = 0;
        submit_form();
    } else {
        // $(".choice-text").on('click', function() {
        //     audio2.play();
        //     audio.play();
        // });
        if (clickedQuit == true) {
            clearInterval(id_quest);
        }
    }
}

update_framequest();

// seterusnya
// $('#div-wrapper').on('click', '.next', function(){
//     next_cnt_quest = parseInt(document.querySelector('.next_cnt_quest').innerText);
//     // alert("next_cnt_ques: " + next_cnt_ques.toString());
//     $.ajax({
//         url: "{% url 'test:test-student' user_type user_id %}",
//         data: {
//             'cnt_quest': next_cnt_quest,
//         },
//         type: 'GET',
//         success: function(result){
//             // alert("Succeed go to next question");
//             $("#div-wrapper").html(result);
//             // var currPlayerAllFieldScoreText = document.querySelector('.span-value-totalScore'); //in player navbar
//             // currPlayerAllFieldScoreText.innerText = document.querySelector('.p-totalPoints_2').innerText;
//             // if (currPlayerAllFieldScoreText.className == "span-value-totalScore correct"){
//             //     currPlayerAllFieldScoreText.className = "span-value-totalScore";
//             // }
//             cnt_quest = parseInt(document.querySelector('.cnt_quest').innerText)
//             $('#progressBarFull').width((cnt_quest/10) * 100 + "%");
//             hasSubmitted = document.querySelector('.hasSubmitted').innerText;
//             i = 0;
//             k = 0;
//             m = 0;
//             // bar_ques = document.querySelector(".div-bar-timer-ques");
//             width_quest = 0;
//             id_quest = 0;
//             // timeLimit = parseInt(document.querySelector('.p-timeLimit').innerText);
//             clickedQuit = false;
//             // clickedHint = false;
//             // clickedHint2 = false;
//             // doneViewHint = false;
//             update_framequest();
//         },
//         error: function(result){
//             // alert("Fail go to next question");
//         }
//     })
// });

// $('#div-wrapper').on('click', '.next', function(){
function nextOnClick(){
    console.log("Yam x comei")
    // next_cnt_quest = parseInt(document.querySelector('.next_cnt_quest').innerText);
    // // alert("next_cnt_ques: " + next_cnt_ques.toString());
    // $.ajax({
    //     url: "{% url 'test:test-student' user_type user_id %}",
    //     data: {
    //         'cnt_quest': next_cnt_quest,
    //     },
    //     type: 'GET',
    //     success: function(result){
    //         // alert("Succeed go to next question");
    //         $("#div-wrapper").html(result);
    //         // var currPlayerAllFieldScoreText = document.querySelector('.span-value-totalScore'); //in player navbar
    //         // currPlayerAllFieldScoreText.innerText = document.querySelector('.p-totalPoints_2').innerText;
    //         // if (currPlayerAllFieldScoreText.className == "span-value-totalScore correct"){
    //         //     currPlayerAllFieldScoreText.className = "span-value-totalScore";
    //         // }
    //         cnt_quest = parseInt(document.querySelector('.cnt_quest').innerText)
    //         $('#progressBarFull').width((cnt_quest/10) * 100 + "%");
    //         hasSubmitted = document.querySelector('.hasSubmitted').innerText;
    //         i = 0;
    //         k = 0;
    //         m = 0;
    //         // bar_ques = document.querySelector(".div-bar-timer-ques");
    //         // width_ques = 0;
    //         id_quest = 0;
    //         // timeLimit = parseInt(document.querySelector('.p-timeLimit').innerText);
    //         clickedQuit = false;
    //         update_frameques();
    //     },
    //     error: function(result){
    //         // alert("Fail go to next question");
    //     }
    // })
}

//lihat keputusan
// $('#div-wrapper').on('click', '.showResult', function(){
//     $.ajax({
//         headers: { "X-CSRFToken": '{{csrf_token}}' }, 
//         url: "{% url 'test:test-student' user_type user_id %}",
//         data: {
//             'requestType': 'updateStatusSessionRecord'
//         },
//         type: 'POST',
//         success: function(response){
//             // alert("updateStatusSessionRecord: success");
//             window.location.href = "{% url 'test:test-student' user_type user_id %}";
//         },
//         error: function(response){
//             // alert("updateStatusSessionRecord: success");
//         }
//     })
// });