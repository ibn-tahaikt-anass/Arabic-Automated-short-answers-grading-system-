import { Component, OnInit } from '@angular/core';
import { Router } from "@angular/router";
import { QuestionService } from '../../services/question-service';
import { AnswerService } from '../../services/answer-service';
import { Answer } from '../../models/answer.model';
import { Question } from '../../models/question.model';

@Component({
  selector: 'app-question-section',
  templateUrl: './question-section.component.html',
  styleUrls: ['./question-section.component.css']
})
export class QuestionSectionComponent implements OnInit {
  currentMaxId = 0;
  isTestVisible = false;
  isInstructionsVisible = true;
  currentQuestionIndex = 0;
  isFinished = false;
  currentQuestion: Question = { id: 0, text_question: '' };
  currentAnswer: Answer = { text_answer: '', question_id: 0, student_id: 0 };
  questions: Question[] = [
   
    { id: 2, text_question: 'ما هي أقصر سورة في القرآن' },
    { id: 3, text_question: 'ما هو اسم زوجة فرعون' },
    { id: 4, text_question: 'كم عام كانت السيدة خديجة تكبر على الرسول صلى الله عليه وسلم' },
    { id: 5, text_question: 'ما هو الثناء على الله' },
    { id: 6, text_question: 'ما هو الرزق' },
    { id: 7, text_question: 'ما هو الرياء' },
    { id: 8, text_question: 'ما هو العمل الصالح' },
    { id: 9, text_question: 'ما هو الصيام' },
    { id: 10, text_question: 'ما الهدف من الدعوة' },
    { id: 11, text_question: 'ما هي الزكاة' },
    { id: 12, text_question: 'عرف الملائكة' }
  ];

  constructor(private QuestionService: QuestionService, private answerService: AnswerService, private router: Router) { }

  ngOnInit(): void {
    this.fetchQuestions();
  }

  startQuiz() {
    this.isTestVisible = true;
    this.isInstructionsVisible = false;
    this.isFinished = false;
  }

  fetchQuestions(): void {
    this.currentQuestion = this.questions[this.currentQuestionIndex];
    this.currentAnswer.question_id = this.currentQuestion.id;
  }

  submitAnswer(): void {
    console.log('Submit button clicked');
    // ... rest of the method
  }
  
}
