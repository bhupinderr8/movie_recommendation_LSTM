import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Component, OnInit } from '@angular/core';
import { PageEvent } from '@angular/material/paginator';
import { Observable } from 'rxjs/internal/Observable';
import { Movie } from '../movie';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent implements OnInit {

  title = 'web-interface';
  movies: Movie[];
  currentMoviesToShow: Movie[];

  constructor(public http: HttpClient){
    this.movies = [];
    this.currentMoviesToShow = [];
  }

  addMovies(){
    let movie: Movie = {
      "writers": [
          {
              "nconst": "nm0124918",
              "primaryname": "Frank Butler"
          },
          {
              "nconst": "nm0491048",
              "primaryname": "Stan Laurel"
          },
          {
              "nconst": "nm0730018",
              "primaryname": "Hal Roach"
          },
          {
              "nconst": "nm0907778",
              "primaryname": "H.M. Walker"
          }
      ],
      "directors": [
          {
              "nconst": "nm0428059",
              "primaryname": "F. Richard Jones"
          },
          {
              "nconst": "nm0946756",
              "primaryname": "Hal Yates"
          }
      ],
      "rating": {
          "averagerating": 7.2,
          "numofvotes": 94
      },
      "primarytitle": "The Nickel-Hopper",
      "originaltitle": "The Nickel-Hopper",
      "titletype": "short",
      "isadult": 0,
      "startyear": 1926,
      "endyear": 12,
      "runtimeminutes": 37,
      "genres": "Comedy,Romance,Short",
      "imagelink": "https://www.viewhotels.jp/ryogoku/wp-content/uploads/sites/9/2020/03/test-img.jpg"
  }

  for(var i = 0; i<10; i++){
    this.movies.push(movie);
  }

  }

  ngOnInit(): void {
    this.addMovies();
  }

  onPageChange($event: PageEvent){
    this.currentMoviesToShow = this.movies.slice(
      $event.pageIndex*$event.pageSize,
      $event.pageIndex*$event.pageSize + $event.pageSize
    );
  }

}
