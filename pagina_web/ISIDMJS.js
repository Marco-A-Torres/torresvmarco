
let indiceSlide =0;
mostrarSlides();

function mostrarSlides(){
	let i=0;
	let slides= PaginaPrincipal.getElementsByClassName("slides");
	for(i=0;i<slides.length;i++){
		slides[i].style.display="none";
	}
	indiceSlide++;
	if(indiceSlide<slides.length){
	   		indiceSlide=1;
	   }
	slides[indiceSlide-1].style.display="block";
	setTimeout(mostrarSlides,2000);
}
