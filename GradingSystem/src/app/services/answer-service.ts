import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Answer } from '../models/answer.model';
import { API_URL } from 'src/env';

@Injectable({
  providedIn: 'root'
})
export class AnswerService {
  private submitAnswersUrl =  `${API_URL}/answers`;
  private fetchAnswersUrl =  `${API_URL}/answers`; 

  constructor(private http: HttpClient) { }

  submitAnswers(answer: Answer, callback: (response: any) => void): void {
    this.http.post<any>(this.submitAnswersUrl, answer).subscribe(response => {
      callback(response);
    });
  }

  fetchAnswers(): Observable<Answer[]> {
    return this.http.get<Answer[]>(this.fetchAnswersUrl);
  }
}
