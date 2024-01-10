import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http'
import { Observable } from 'rxjs';
import { API_URL } from 'src/env';


@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private BASE_URL: string = `${API_URL}/auth`;
  constructor(private http: HttpClient) {}
 
  
}

