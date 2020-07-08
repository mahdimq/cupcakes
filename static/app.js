const BASE_URL = 'http://127.0.0.1:5000'

$cupcakeDisplay = $('#cupcake-display') //<-- div where HTML will populate to

// Populate page with cupcakes currently in the DB
function populateHTML(cupcake) {
	return `
    <div data-id=${cupcake.id} class="col-sm-6 col-md-4 col-lg-3">
      <h4>${cupcake.flavor}</h4>
      <p class="my-0">Cupcake Rating: <strong>${cupcake.rating}</strong></p>
      <p>Cupcake Size: ${cupcake.size}</p>
      <img class="img-thumbnail rounded mx-auto d-block" src="${cupcake.image}" alt="cupcake image">
      <button id="delete" class="btn btn-danger mt-2">Delete</button>
      <hr>
    </div>
    `
}

// logic to show cupcakes from database
async function showCupcakes() {
	const res = await axios.get(`${BASE_URL}/api/cupcakes`)
	for (let data of res.data.cupcakes) {
		//<-- loop over json
		let cupcake = populateHTML(data) //<-- set populateHTML funtion to var
		$cupcakeDisplay.append(cupcake) //<-- append to html
	}
}

// add a new cupcake and commit it to database
$('.cupcake-form').submit(async function (e) {
	e.preventDefault() //<-- stops page from refreshing
	let flavor = $('#flavor').val() //<-- get input value from form
	let size = $('#size').val() //<-- get input value from form
	let rating = parseInt($('#rating').val()) //<-- get input value from form
	let image = $('#image').val() //<-- get input value from form

	const res = await axios.post(`${BASE_URL}/api/cupcakes`, { flavor, size, rating, image })
	let newCupcake = populateHTML(res.data.cupcake) //<-- adds data to popHTML function
	$cupcakeDisplay.append(newCupcake) //<-- populates HTML with data
	$('.cupcake-form').trigger('reset')
})

// delete a cupcake from database and remove from HTML page
$('#cupcake-display').on('click', '#delete', async function (e) {
	e.preventDefault() //<-- stops page from refreshing
	let cupcakeDiv = $(e.target).closest('div') //<-- selects closest div to target
	let cupcakeId = cupcakeDiv.attr('data-id') //<-- selects is based on data-id attr
	await axios.delete(`${BASE_URL}/api/cupcakes/${cupcakeId}`) //<-- deletes from DB
	cupcakeDiv.remove() //<-- removes data from HTML DOM
})

showCupcakes() //<-- runs the show cupcakes functions
