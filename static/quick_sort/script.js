var container = document.getElementById("array");
var arr=[];

// Function to generate the array of blocks
function Userarray() {
    val = document.getElementById("arry").value;
    arr = val.split(",");

// Calling generatearray function
    generatearray(arr);


}
// Calling QuickSort function
function qsort() {

QuickSort(0, arr.length-1);
}


function generatearray(arr) {

	document.getElementById("array").innerHTML="";


	for (var i = 0; i < arr.length; i++) {
			var value=arr[i];
		// Creating element div
		var array_ele = document.createElement("div");

		// Adding class 'block' to div
		array_ele.classList.add("block");

		// Adding style to div
		array_ele.style.height =
		`${value * 3}px`;
		array_ele.style.transform =
		`translate(${i * 30}px)`;

		// Creating label element for displaying
		// size of particular block
		var array_ele_label =
		document.createElement("label");
		array_ele_label.classList.add("block_id");
		array_ele_label.innerText = value;

		// Appending created elements to merge.html
		array_ele.appendChild(array_ele_label);
		container.appendChild(array_ele);
	}
}



async function hoare_partition(l, r, delay = 75) {
	delay=document.getElementById("myRange").value;
	var blocks =
	document.querySelectorAll(".block");
	var pivot =
	Number(blocks[l].childNodes[0].innerHTML);

	var i = l - 1;
	var j = r + 1;

	while (true) {
		// Find leftmost element greater than
		// or equal to pivot
		do {
			i++;
			if (i - 1 >= l) blocks[i - 1].style.backgroundColor = "red";
			blocks[i].style.backgroundColor = "yellow";
			//To wait for 700 milliseconds
			await new Promise((resolve) =>
				setTimeout(() => {
					resolve();
				}, delay)
			);
		} while (Number(blocks[i].childNodes[0].innerHTML) < pivot);

		// Find rightmost element smaller than
		// or equal to pivot
		do {
			j--;
			if (j + 1 <= r) blocks[j + 1].style.backgroundColor = "green";
			blocks[j].style.backgroundColor = "yellow";
			//To wait for 700 milliseconds
			await new Promise((resolve) =>
				setTimeout(() => {
					resolve();
				}, delay)
			);
		} while (Number(blocks[j].childNodes[0].innerHTML) > pivot);

		// If two pointers met.
		if (i >= j) {
			for (var k = 0; k < arr.length; k++) blocks[k].style.backgroundColor = "rgb(49, 226, 13)";
			return j;
		}


		//swapping ith and jth element
		var temp1 = blocks[i].style.height;
		var temp2 = blocks[i].childNodes[0].innerText;
		blocks[i].style.height = blocks[j].style.height;
		blocks[j].style.height = temp1;
		blocks[i].childNodes[0].innerText = blocks[j].childNodes[0].innerText;
		blocks[j].childNodes[0].innerText = temp2;
		//To wait for 700 milliseconds
		await new Promise((resolve) =>
			setTimeout(() => {
				resolve();
			}, delay)
		);
	}

}

// Asynchronous QuickSort function
async function QuickSort(l, r, delay = 100) {
		flag=0;
	timer1();
	// QuickSort Algorithm
	if (l < r) {
		//Storing the index of pivot element after partition
		var pivot_idx = await hoare_partition(l, r);
		//Recursively calling quicksort for left partition
		await QuickSort(l, pivot_idx);
		//Recursively calling quicksort for right partition
		await QuickSort(pivot_idx + 1, r);
	}
	// To enable the button "Generate New Array" after final(sorted)
      document.getElementById("Enter").disabled = false;
      document.getElementById("Enter").style.backgroundColor = "#37517e";

      // To enable the button "Selection Sort" after final(sorted)
      document.getElementById("sort").disabled = false;
      document.getElementById("sort").style.backgroundColor = "#37517e";

      //To enable the button generate random
      document.getElementById("gr").disabled = false;
      document.getElementById("gr").style.backgroundColor = "#37517e";
      flag=1;
}
	var flag=0;
function Randomarray() {

	// arr=[50,10,20,40,30];
	// arr=[];
	arr=[1,1,1,1,1,1,1,1,1,1]
	document.getElementById("array").innerHTML="";
	for (var i = 0; i <=10; i++) {
		// Return a value from 1 to 100 (both inclusive)

			var value=Math.floor(Math.random() * 100) + 1;


		arr[i]=value;





		// Creating element div





		var array_ele = document.createElement("div");

		// Adding class 'block' to div
		array_ele.classList.add("block");

		// Adding style to div
		array_ele.style.height =
		`${value * 3}px`;
		array_ele.style.transform =
		`translate(${i * 30}px)`;

		// Creating label element for displaying
		// size of particular block
		var array_ele_label =
		document.createElement("label");
		array_ele_label.classList.add("block_id");
		array_ele_label.innerText = value;

		// Appending created elements to merge.html
		array_ele.appendChild(array_ele_label);
		container.appendChild(array_ele);
	}
}
  function disable()
    {
      // To disable the button "Generate New Array"
      document.getElementById("Enter").disabled = true;
      document.getElementById("Enter").style.backgroundColor = "#AED6F1";

      // To disable the button "Selection Sort"
      document.getElementById("sort").disabled = true;
      document.getElementById("sort").style.backgroundColor = "#AED6F1";
      //To disable the button generate random
      document.getElementById("gr").disabled = true;
      document.getElementById("gr").style.backgroundColor = "#AED6F1";
    }


