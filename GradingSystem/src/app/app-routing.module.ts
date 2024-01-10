import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { RegisterComponent } from './components/register/register.component';
import { HomeComponent } from './components/home/home.component';
import { QuestionSectionComponent } from './components/question-section/question-section.component';
import { LoginComponent } from './components/login/login.component';
import { ReviewComponent } from './components/review/review.component';
const routes: Routes = [
  {
    path : 'register',
    component : RegisterComponent
  },
  {
    path : 'login',
    component : LoginComponent
  },
  {
    path : 'home',
    component : HomeComponent
  },
  {
    path : '',
    component : HomeComponent
  },
  {
    path : 'exam',
    component : QuestionSectionComponent
  },
  {
    path : 'review',
    component : ReviewComponent
  }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
