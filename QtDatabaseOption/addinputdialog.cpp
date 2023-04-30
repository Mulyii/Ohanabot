#include "addinputdialog.h"
#include <QPushButton>
AddInputDialog::AddInputDialog(const QStringList &options,QWidget *parent)
    :QDialog(parent)
{
    this->setWindowTitle("添加记录");

    QFormLayout *formLayout = new QFormLayout(this);
    for(int i=0;i<options.size();i++)
    {
        QLineEdit *lineEdit = new QLineEdit(this);
        formLayout->addRow(options[i]+":",lineEdit);
        lineEdits.append(lineEdit);
    }


    QPushButton *okButton = new QPushButton("OK",this);
    formLayout->addRow(okButton);
    connect(okButton,&QPushButton::clicked,this,&QDialog::accept);
    QPushButton *cancelButton = new QPushButton("Cancel", this);
        formLayout->addRow(cancelButton);
        connect(cancelButton, &QPushButton::clicked, this, &QDialog::reject);
}
QList<QString> AddInputDialog::getInputs() const
{
    QList<QString> inputs;
    for (QLineEdit *lineEdit : lineEdits) {
        inputs.append(lineEdit->text());
    }
    return inputs;
}
AddInputDialog::~AddInputDialog()
{
    for (QLineEdit *lineEdit : lineEdits) {
        delete lineEdit;
    }
}
