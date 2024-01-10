import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http'
import { Observable } from 'rxjs';
import { Question } from '../models/student.model';
import { API_URL } from 'src/env';

@Injectable({
  providedIn: 'root'
})

export class QuestionService {
   
        private fetchQuestionsUrl = `${API_URL}/questions`; // modify URL to match your backend API
        
        constructor(private http: HttpClient) { }
      
        fetchQuestions(): Observable<Question[]> {
          return this.http.get<Question[]>(this.fetchQuestionsUrl);
        }
      }

