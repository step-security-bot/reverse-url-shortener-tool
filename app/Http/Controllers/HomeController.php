<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;

class HomeController extends Controller
{
    // __invoke for single action controllers
    public function __invoke()
    {
        return view('index');
    }
}
