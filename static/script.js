let num = parseInt(prompt('Enter the number of data you want to generate'));
let mean = parseInt(prompt('Enter the Mean of data you want to generate'));
let va = parseInt(prompt('Enter the Variance of data you want to generate'))
        let linkk = "http://127.0.0.1:5000/normal/"
        num = num.toString();
        mean = mean.toString();
        va = va.toString();
        linkk = linkk.concat(mean)
        linkk = linkk.concat('/')
        linkk = linkk.concat(va)
        linkk = linkk.concat('/')
        linkk = linkk.concat(num)
console.log(linkk)

fetch(linkk)
			.then(response => response.json())
			.then(data => {
				const tableBody = document.querySelector('#uniform-table tbody');
				const numCols = 4;
				let row;

				data.data.forEach((value, index) => {
					if (index % numCols === 0) {
						row = tableBody.insertRow();
					}

					const cell = row.insertCell();
					cell.appendChild(document.createTextNode(value));
				});
			})
			.catch(error => console.error(error));

		//Add event listener for the download button
		const downloadBtn = document.querySelector('#download-csv');
		downloadBtn.addEventListener('click', () => {
			const rows = document.querySelectorAll('#uniform-table tr');
			let csv = [];
			for (const row of rows) {
				const rowData = [];
				const cols = row.querySelectorAll('td');
				for (const col of cols) {
					rowData.push(col.textContent.trim());
				}
				csv.push(rowData.join(','));
			}
			csv = csv.join('\n');
			const link = document.createElement('a');
			link.setAttribute('href', 'data:text/csv;charset=utf-8,' + encodeURIComponent(csv));
			link.setAttribute('download', 'uniform-data.csv');
			document.body.appendChild(link);
			link.click();
			document.body.removeChild(link);
		});

