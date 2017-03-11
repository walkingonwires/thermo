$(document).ready(function () {
    var $curTempView = $('#currentTemp'),
        $targTempView = $('#targetTemp'),
        localTarget = null,
        officialTarget = null,
        currentPiTemp = null;
            
    

    function getCurrentTemp () {
        $.get('/current-temp').then(function (res) {
            res = JSON.parse(res);
            $curTempView.text(res.currentTemp);
        }).catch(function (err) {
            console.warn("didn't get temp \n" + err);
        });
    }
    
    function getTargetTemp() {
        
    }

    function updateTargetTemp() {
        
    }
    
    function increaseTargetTemp() {
        
    }
    
    function decreaseTargetTemp() {
        
    }
    
    function toggleMode () {
        
    }

    getCurrentTemp()
    
    

});