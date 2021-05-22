// USando o local storage, se o usuário sair do browser ou dar F5 e voltar a contagem continua
if (!localStorage.getItem("counter")) {
	localStorage.setItem("counter", 0);
}

//let counter = 0;

function count() {
	let counter = localStorage.getItem("counter");
	
	counter++;
	
	document.querySelector("h1").innerHTML = counter;
	localStorage.setItem("counter", counter);
	
	if (counter % 10 === 0) {
		// Backtick funciona como o f"" do python ou $"" do C# e permite interpolar strings
		alert(`Count is now ${counter}`);
	}
}

//Este event listner serve para indicar quando o HTML está totalmente carregado
document.addEventListener("DOMContentLoaded", function () {
	// Quando o documento estiver carregado, associe a função click ao click do botão.
	// Note que não chamamos a função count() com parenteses, apenas associamos a propria função ao event handler
	//   document.querySelector("button").addEventListener('click', count); // desta forma ou como abaixo dá na mesma
	document.querySelector("h1").innerHTML = localStorage.getItem('counter');
	document.querySelector("button").onclick = count;
});
