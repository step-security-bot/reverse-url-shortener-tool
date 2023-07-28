<?php

use App\Http\Controllers\HomeController;
use App\Http\Controllers\PostsController;
use Illuminate\Support\Facades\Route;

// GET
Route::get('/blog', [PostsController::class, 'index']);
Route:: get('/blog/{id}', [PostsController::class, 'show']); // {id?} = default value

// POST
Route::get('/blog/create', [PostsController::class, 'create']);
Route:: post('/blog/{id}', [PostsController::class, 'store']);

// PUT OR PATCH
Route::get('/blog/edit/{id}', [PostsController::class, 'edit']);
Route:: patch('/blog/{id}', [PostsController::class, 'update']);

// GET
Route::get('/blog', [PostsController::class, 'index']);
Route:: get('/blog/{id}', [PostsController::class, 'show']);

// DELETE
Route::delete('/blog/{id}', [PostsController::class, 'destroy']);

// Route::resource('blog', PostsController::class); // ::class = 'App\Http\Controllers\PostsController'

// Route for invoke method
Route::get('/', HomeController::class);

/*
|--------------------------------------------------------------------------
| Web Routes
|--------------------------------------------------------------------------
|
| Here is where you can register web routes for your application. These
| routes are loaded by the RouteServiceProvider and all of them will
| be assigned to the "web" middleware group. Make something great!
|
|--------------------------------------------------------------------------
| 
| GET - Request a resource
| POST - Create a new resource
| PUT - Update a resource
| PATCH - Modify a resource
| DELETE - Delete a resource
| OPTIONS - Ask the server wich verbs are allowed
|
|--------------------------------------------------------------------------
|--------------------------------------------------------------------------
| Multiple HTTP verbs
|--------------------------------------------------------------------------
| 
| Route::match(['GET', 'POST'], '/blog', [PostsController::class, 'index']);
| Route::any(['/blog', [PostsController::class, 'index']);
|
|--------------------------------------------------------------------------
|--------------------------------------------------------------------------
| Return view
|--------------------------------------------------------------------------
| Route::view('/blog', 'blog.index', ['name' => 'Code with me']);
|--------------------------------------------------------------------------
*/
