import { Component } from '@angular/core';
import { AnswerService } from '../../services/answer-service';
import { GradeService } from '../../services/grade-service';
import { QuestionService } from '../../services/question-service';
import { Answer } from '../../models/answer.model';
import { Grade } from '../../models/grade.model';
import { Question } from '../../models/student.model';

@Component({
  selector: 'app-review',
  templateUrl: './review.component.html',
  styleUrls: ['./review.component.css']
})
export class ReviewComponent {

  answers!: Answer[] ;
  grades!: Grade[] ;
  questions!: Question[] ;
  totalScore = 0;
  moy=this.totalScore/10;
  
  constructor(
    private answerService: AnswerService,
    private gradeService: GradeService,
    private questionService: QuestionService  ) { }
  ngOnInit(): void {
    this.fetchAnswers();
    this.fetchQuestions();
    this.fetchGrades();
  }
  fetchAnswers() {
    this.answerService.fetchAnswers()
      .subscribe(answers => {
        this.answers = answers;
        this.fetchGrades();
      });
  }
  fetchQuestions() {
    this.questionService.fetchQuestions()
      .subscribe(questions => this.questions = questions);
  }
  fetchGrades() {
    this.gradeService.fetchGrades()
      .subscribe(grades => {
        this.grades = grades;
        this.calculateScore();
      });
  }
  calculateScore(): void {
    this.totalScore = this.grades.reduce((total, grade) => total + grade.score, 0);
    this.moy=this.totalScore/2.5;

  }
  getQuestionText(questionId: number): string {
    return this.questions.find(question => question.id === questionId)?.text_question || '';
  }

  getAnswerText(answer_id: number): string {
    const answer = this.answers[answer_id];
    return answer?.text_answer ?? 'jjjj';  }

    getScore(answerId: number): number {
      console.log('answerId:', answerId);
      console.log('grades:', this.grades);
      const grade = this.grades.find(g => g.answer_id === answerId);
      return grade?.score ?? 0;
    }
  
}
