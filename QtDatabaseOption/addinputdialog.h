#ifndef ADDINPUTDIALOG_H
#define ADDINPUTDIALOG_H

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
#include <QLabel>
class AddInputDialog:public QDialog
{
public:
    explicit AddInputDialog(const QStringList &options,QWidget *parent );
    QList<QString>getInputs() const;
    ~AddInputDialog();
private:
    QList<QLineEdit*>lineEdits;

};

#endif // ADDINPUTDIALOG_H
