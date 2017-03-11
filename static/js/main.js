$(document).ready(function () {
    var $piCurrentTempView = $('#piCurrentTemp'),
        $piTargetTempView = $('#piTargetTemp'),
        $thermoCurrentTempView = $('#thermoCurrentTemp'),
        $thermoTargetTempView = $('#thermoTargetTemp');
            
    
    var thermo = {
        getCurrentTemp: function () {
        },
        getTargetTemp: function () {

        },
        setTargetTemp: function () {

        },

        setMode: function () {

        },
        setFan: function () {

        }
    };

    var pi = {
        getCurrentTemp: function () {
            return $.get('/current-temp').then(function (res) {
                console.log(typeof res, res);
                res = JSON.parse(res);
                return res.currentTemp;
            }).catch(function (err) {
                console.warn("didn't get temp \n" + err);
                return err;
            });
        },
        getTargetTemp: function () {},
        setTargetTemp: function () {

        }
    };

    function updateViewVals (element, val) {
        element.text(addDegrees(val));
    }

    function addDegrees(temp) {
        return '' + temp + String.fromCharCode(176);
    }



    pi.getCurrentTemp().then(function (temp) {
        updateViewVals($piCurrentTempView, temp);
    })

});