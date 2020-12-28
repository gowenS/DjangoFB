var canvas = document.querySelector('canvas');
//canvas.height = window.innerHeight * 0.65 ;
//console.log('Height is: ' + canvas.height);
//canvas.width = canvas.height * 0.8;
//console.log('Width is: ' + canvas.width);
var c = canvas.getContext('2d');
var paint = false;
var mouseX;
var mouseY;
var touchX;
var touchY;
var onCanvas = false;
var penSize = 3;
var linePoints = new Array();
var lines = new Array();
var color = 'black';
var linesWeight = new Array();
var linesColor = new Array();



canvas.addEventListener('touchstart', function(event){
	paint = true;
	touchX = event.touches[0].pageX - this.offsetLeft;
	touchY = event.touches[0].pageY - this.offsetTop;
	linePoints.push(touchX);
	linePoints.push(touchY);
	draw();
})

canvas.addEventListener('touchmove', function(event){
	event.preventDefault();
	paint = true;
	touchX = event.touches[0].pageX - this.offsetLeft;
	touchY = event.touches[0].pageY - this.offsetTop;
	linePoints.push(touchX);
	linePoints.push(touchY);
	draw();
		
	
})

canvas.addEventListener('touchend', function(event){
	paint = false;
	lines.push(linePoints);
	linePoints = new Array();
	linesWeight.push(penSize);
	linesColor.push(color);
	draw();		
	
})

canvas.addEventListener('touchcancel', function(event){
	if(paint) {
		lines.push(linePoints);
		linePoints = new Array();
		linesWeight.push(penSize);
		linesColor.push(color);
		draw();
	}
	paint = false;		
	
})


canvas.addEventListener('mouseover', function(event){
	onCanvas = true;
})

canvas.addEventListener('mouseleave', function(event){
	onCanvas = false;
	if(paint) {
		lines.push(linePoints);
		linePoints = new Array();
		linesWeight.push(penSize);
		linesColor.push(color);
		draw();
	}
	paint = false;
	
})

canvas.addEventListener('mouseup', function(event){
	paint = false;
	lines.push(linePoints);
	linePoints = new Array();
	linesWeight.push(penSize);
	linesColor.push(color);
	draw();
})

canvas.addEventListener('mousemove', function(event){
	if(onCanvas && paint){
		mouseX = event.pageX - this.offsetLeft;
		mouseY = event.pageY - this.offsetTop;
		linePoints.push(mouseX);
		linePoints.push(mouseY);		
	}
	draw();
})

canvas.addEventListener('mousedown', function(event){
	if(onCanvas) paint = true;
	mouseX = event.pageX - this.offsetLeft;
	mouseY = event.pageY - this.offsetTop;
	linePoints.push(mouseX);
	linePoints.push(mouseY);
	draw();
	
})

function deleteLine(){
	if(lines.length > 0) {
		var copy = new Array();
		var copyWeights = new Array();
		var copyColors = new Array();
		for (var i = 0; i < lines.length - 1; i++){
			copy[i] = lines[i];
			copyWeights[i] = linesWeight[i];
			copyColors[i] = linesColor[i];
		}
		lines = copy;
		linesWeight = copyWeights;
		linesColor = copyColors;
	}
	draw();
}

function changeLineWeight(input){
	if(input == "fine") penSize = 1;
	if(input == "medium") penSize = 5;
	if(input == "bold") penSize = 12;
}

function changeLineColor(input){
	if(input == "black") color = 'black';
	if(input == "red") color = '#F80707';
	if(input == "blue") color = '#3498DB';
	if(input == "green") color = '#2ECC71';
	if(input == "yellow") color = '#F1C40F';
}

function draw(){
	
	c.clearRect(0, 0 , c.canvas.width, c.canvas.height);
	
	for(var i = 0; i < lines.length ; i++){
		c.beginPath();
		var curLine = lines[i];
		c.moveTo(curLine[0],curLine[1]);
		if(curLine.length > 2){
			for(var j = 0; j < curLine.length; j++){
				c.lineTo(curLine[j], curLine[j+1]);
				j++;
				
			}
			c.lineWidth = linesWeight[i];
			c.strokeStyle = linesColor[i];
			c.stroke();
//			console.log('Drawing');
			
		} 
		
	}
	c.beginPath();
	c.moveTo(linePoints[0],linePoints[1]);
	for(var j = 0; j < linePoints.length; j++){
		c.lineTo(linePoints[j], linePoints[j+1]);
		j++;
	}
	c.lineWidth = penSize;
	c.strokeStyle = color;
	c.stroke();
//	console.log('Drawing');
	
	
}