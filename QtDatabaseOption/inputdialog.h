#ifndef INPUTDIALOG_H
#define INPUTDIALOG_H
#include <QApplication>
#include <QDialog>
#include <QFormLayout>
#include <QComboBox>
#include <QLineEdit>
#include <QPushButton>
#include <QObject>
#include <QWidget>
#include <QString>
#include <QStringList>
class InputDialog: public QDialog
{
public:
    InputDialog(const QString &s,const QStringList &sl,QWidget *parent );
    QString getText() const;

    QString getItem() const;

private:
    QString text;
    QString item;
    QComboBox comboBox;
    QLineEdit lineEdit;
};

#endif // INPUTDIALOG_H
