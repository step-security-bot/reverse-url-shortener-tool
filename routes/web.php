<?php

use App\Http\Controllers\FallbackController;
use App\Http\Controllers\HomeController;
use App\Http\Controllers\PostsController;
use Illuminate\Support\Facades\Route;

// Route:: get('/blog/{id}/{name}', [PostsController::class, 'show']) // {id?} = default value
//     ->whereNumber('id')
//     ->whereAlpha('name'); // https://laravel.com/docs/10.x/routing#parameters-regular-expression-constraints


Route::prefix('blog/')->group(function () {
    // GET
    Route::get('/', [PostsController::class, 'index'])->name('blog.index');
    Route::get('/{id}', [PostsController::class, 'show'])->name('blog.show');
    // POST
    Route::get('/create', [PostsController::class, 'create'])->name('blog.create');
    Route::post('/', [PostsController::class, 'store'])->name('blog.store');
    // PUT OR PATCH
    Route::get('/edit/{id}', [PostsController::class, 'edit'])->name('blog.edit');
    Route::patch('/{id}', [PostsController::class, 'update'])->name('blog.update');
    // DELETE
    Route::delete('/{id}', [PostsController::class, 'destroy'])->name('blog.destroy');
});

// Route::resource('blog', PostsController::class); // ::class = 'App\Http\Controllers\PostsController'

// Route for invoke method
Route::get('/', HomeController::class);

// Fallback Route
Route::fallback(FallbackController::class);

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
