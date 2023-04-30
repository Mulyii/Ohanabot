#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include <QDateTime>
#include <QtSql/QSqlDatabase>
#include <QSqlQuery>
#include <QSqlError>
#include <QtWidgets>
#include <QVector>
#include <QtAlgorithms>
#include <QSqlRecord>
#include <QDate>
#include <QTime>
#include <QInputDialog>
#include <QStringList>
#include <QMessageBox>
#include "inputdialog.h"
#include "addinputdialog.h"
QT_BEGIN_NAMESPACE
namespace Ui { class MainWindow; }
QT_END_NAMESPACE

class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    MainWindow(QWidget *parent = nullptr);
    ~MainWindow();
    void showTables() ;//主窗口显示
    void showScoresTables();//展示成绩
    void showContestTables();//展示比赛
    void showUsersTables();//展示用户
private slots:
    void on_comboBox_currentTextChanged(const QString &arg1);
    void on_pushButton_clicked();
    void onTableItemChanged(int row,int column);
    void on_addPushButton_clicked();
    void deleteRow(int);
private:
    QString table;
    Ui::MainWindow *ui;
    QSqlDatabase db;

};
#endif // MAINWINDOW_H
