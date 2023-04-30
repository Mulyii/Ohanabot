#include "inputdialog.h"

InputDialog::InputDialog(const QString &s,const QStringList &sl,QWidget *parent)
    :QDialog(parent)
{

    QFormLayout *formLayout = new QFormLayout(this);
    this->setWindowTitle(s+"表查询");
    comboBox.addItems(sl);
    formLayout->addRow("选择字段:",&comboBox);

    formLayout->addRow("请输入字段值:",&lineEdit);

    QPushButton *okButton = new QPushButton("OK",this);
    formLayout->addRow(okButton);
    connect(okButton,&QPushButton::clicked,this,&QDialog::accept);
    connect(this,&QDialog::rejected,[](){});
}

QString InputDialog::getText() const
{
    return lineEdit.text();
}

QString InputDialog::getItem() const
{
    return comboBox.currentText();
}
