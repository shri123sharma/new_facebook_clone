var text = document.getElementsByTagName('textarea')[0],
    more = document.getElementsByClassName('more')[0],
    cont =document.getElementById('body'),
    areaCont = document.getElementsByClassName('imtcontainer')[0],
    ico = document.querySelectorAll(".photos , .feeling, .tagfriend, .checkin, .back, .live "),
    line = document.querySelectorAll('.line span'),
    bor =document.querySelectorAll('.line')
    exit = document.querySelectorAll('.title p')[0],
    colo = document.getElementsByClassName('colors')
    span = document.querySelectorAll('.colors span'),
    footer= document.getElementsByClassName('footer')[0];
    

text.onfocus = function(){
	
	text.style.height = "90px";
	cont.classList.add('clicked');
	areaCont.classList.add('area');
    document.getElementsByClassName('mainDiv')[0].classList.add('area');
       more.style.display = "none"
       ico[2].style.display = 'inline-block';
       ico[3].style.display = 'inline-block';
       ico[4].style.display = 'inline-block';
       ico[5].style.display = 'inline-block';


	for(var i = 0; i<ico.length; i++){
	ico[i].classList.add('opwidth');
   }


   bor[0].style.borderTop= 'none';
    bor[0].style.borderBottom= '1px solid #e9ebee';
    footer.style.display='block';

}




exit.onclick = function(){
		footer.style.display='none';
	text.style.height = "";

	cont.classList.remove('clicked');
	
	areaCont.classList.remove('area');
   
    more.style.display = "inline-block"
    
    ico[2].style.display = 'none';
    ico[3].style.display = 'none';
	ico[4].style.display = 'none';
    ico[5].style.display = 'none';
	
	for(var i = 0; i<ico.length; i++){
	ico[i].classList.remove('opwidth');
   }
   for(var i=0; i<line.length; i++){
   line[i].style.display= "none";
}
 text.value= '';
  text.placeholder= " what's in your mind?";

}


ico[5].onclick=function(){
     
	colo[0].classList.toggle('visible');

	  for(var i=0; i<line.length; i++){
   line[i].style.display= "inline-block";
}
}









var col = ['#e8eaee','#fcd85d', '#f25467', '#10aaff', '#f25467', '#488ee8','#5a3be2',
'#5e6574'];


span[0].onclick=function(){
	text.style.backgroundColor=col[0];
	text.style.color="#333";
};
span[1].onclick=function(){
	text.style.backgroundColor=col[1];
	text.style.color="#fff";
};
span[2].onclick=function(){
	text.style.backgroundColor=col[2];
	text.style.color="#fff";
};
span[3].onclick=function(){
	text.style.backgroundColor=col[3];
	text.style.color="#fff";
};
span[4].onclick=function(){
	text.style.backgroundColor=col[4];
	text.style.color="#fff";
};
span[5].onclick=function(){
	text.style.backgroundColor=col[5];
	text.style.color="#fff";
};
span[6].onclick=function(){
	text.style.backgroundColor=col[6];
	text.style.color="#fff";
};
span[7].onclick=function(){
	text.style.backgroundColor=col[7];
	text.style.color="#fff";
};












 function InputAdjust(o) {
        o.style.height = "1px";
        o.style.height = (40+o.scrollHeight)+"px";
    }