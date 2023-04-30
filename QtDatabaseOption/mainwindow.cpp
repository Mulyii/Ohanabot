#include "mainwindow.h"
#include "ui_mainwindow.h"
#include <QTableWidget>
MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent)
    , ui(new Ui::MainWindow)
{
    ui->setupUi(this);
    db = QSqlDatabase::addDatabase("QODBC");
    db.setHostName("localhost");
    db.setPort(3306);
    db.setDatabaseName("robot");
    db.setUserName("root");
    db.setPassword("root");
    bool ok = db.open();
    if (ok){
        qDebug() << "success!!";
    }
    else {
        qDebug() << "open failed";
        qDebug() << "error open database because" << db.lastError().text();
    }
    table = ui->comboBox->currentText();
    connect(ui->tableWidget,&QTableWidget::cellDoubleClicked,this,&MainWindow::onTableItemChanged);
    showTables();
}

MainWindow::~MainWindow()
{
    delete ui;
}

//响应查询按钮
void MainWindow::on_comboBox_currentTextChanged(const QString &arg1)
{
    table = arg1;
    qDebug()<<table<<'\n';
    showTables();
}



//展示成绩
void MainWindow::showScoresTables()
{
    table = ui->comboBox->currentText();
    ui->tableWidget->setColumnCount(6);
    //建立表头
    QStringList header;
    header << "contestId" << "userId" << "rank" << "number"<<"penalty"<<"isDelete";
    ui->tableWidget->setHorizontalHeaderLabels(header);
    ui->tableWidget->horizontalHeader()->setSectionResizeMode(QHeaderView::Stretch);
    QSqlQuery query=db.exec("select * from scores");;
    while(query.next())
    {
        int rowCount = ui->tableWidget->rowCount();
        ui->tableWidget->insertRow(rowCount);
        QString contestId=query.value("contestid").toString();
        QString userId=query.value("userid").toString();
        QString rank = query.value("rank").toString();
        QString number = query.value("number").toString();
        QString penalty = query.value("penalty").toString();
        ui->tableWidget->setItem(ui->tableWidget->rowCount()-1,0,new QTableWidgetItem(contestId));
        ui->tableWidget->setItem(ui->tableWidget->rowCount()-1,1,new QTableWidgetItem(userId));
        ui->tableWidget->setItem(ui->tableWidget->rowCount()-1,2,new QTableWidgetItem(rank));
        ui->tableWidget->setItem(ui->tableWidget->rowCount()-1,3,new QTableWidgetItem(number));
        ui->tableWidget->setItem(ui->tableWidget->rowCount()-1,4,new QTableWidgetItem(penalty));
        QPushButton* deleteButton = new QPushButton("删除");
        ui->tableWidget->setCellWidget(ui->tableWidget->rowCount()-1,5, deleteButton);
        int row = ui->tableWidget->rowCount()-1;
        connect(deleteButton, &QPushButton::clicked, this,[this, row]() {
                deleteRow(row);
            });

    }
    query.clear();
}


//展示比赛
void MainWindow::showContestTables()
{
    table = ui->comboBox->currentText();
    ui->tableWidget->setColumnCount(6);
    //建立表头
    QStringList header;
    header << "contestId" << "contestName" << "time" << "duration"<<"site"<<"isDelete";
    ui->tableWidget->setHorizontalHeaderLabels(header);
    ui->tableWidget->horizontalHeader()->setSectionResizeMode(QHeaderView::Stretch);
    QSqlQuery query=db.exec("select * from contests");;
    while(query.next())
    {
        int rowCount = ui->tableWidget->rowCount();
        ui->tableWidget->insertRow(rowCount);
        QString contestId=query.value("contestid").toString();
        QString contestName=query.value("contestname").toString();
        QString time = query.value("time").toDateTime().toString("yyyy-MM-dd hh:mm:ss");
        QString duration = query.value("duration").toTime().toString("hh:mm:ss");
        QString site = query.value("site").toString();
        ui->tableWidget->setItem(ui->tableWidget->rowCount()-1,0,new QTableWidgetItem(contestId));
        ui->tableWidget->setItem(ui->tableWidget->rowCount()-1,1,new QTableWidgetItem(contestName));
        ui->tableWidget->setItem(ui->tableWidget->rowCount()-1,2,new QTableWidgetItem(time));
        ui->tableWidget->setItem(ui->tableWidget->rowCount()-1,3,new QTableWidgetItem(duration));
        ui->tableWidget->setItem(ui->tableWidget->rowCount()-1,4,new QTableWidgetItem(site));
        QPushButton* deleteButton = new QPushButton("删除");
        ui->tableWidget->setCellWidget(ui->tableWidget->rowCount()-1,5, deleteButton);
        int row = ui->tableWidget->rowCount()-1;
        connect(deleteButton, &QPushButton::clicked, this,[this, row]() {
                deleteRow(row);
            });

    }
    query.clear();
}
//展示用户
void MainWindow::showUsersTables()
{
    table = ui->comboBox->currentText();
    ui->tableWidget->setColumnCount(7);
    //建立表头
    QStringList header;
    header << "userId" << "realName" << "qq" << "stuId"<<"codeforces"<<"missionid"<<"isDelete";
    ui->tableWidget->setHorizontalHeaderLabels(header);
    ui->tableWidget->horizontalHeader()->setSectionResizeMode(QHeaderView::Stretch);
    QSqlQuery query=db.exec("select * from users");;
    while(query.next())
    {
        int rowCount = ui->tableWidget->rowCount();
        ui->tableWidget->insertRow(rowCount);
        QString userId=query.value("userid").toString();
        QString realName=query.value("realname").toString();
        QString qq = query.value("qq").toString();
        QString stuId = query.value("stuid").toString();
        QString codeforces = query.value("codeforces").toString();
        QString missionId = query.value("missionid").toString();
        ui->tableWidget->setItem(ui->tableWidget->rowCount()-1,0,new QTableWidgetItem(userId));
        ui->tableWidget->setItem(ui->tableWidget->rowCount()-1,1,new QTableWidgetItem(realName));
        ui->tableWidget->setItem(ui->tableWidget->rowCount()-1,2,new QTableWidgetItem(qq));
        ui->tableWidget->setItem(ui->tableWidget->rowCount()-1,3,new QTableWidgetItem(stuId));
        ui->tableWidget->setItem(ui->tableWidget->rowCount()-1,4,new QTableWidgetItem(codeforces));
        ui->tableWidget->setItem(ui->tableWidget->rowCount()-1,5,new QTableWidgetItem(missionId));
        QPushButton* deleteButton = new QPushButton("删除");
        ui->tableWidget->setCellWidget(ui->tableWidget->rowCount()-1,6, deleteButton);
        int row = ui->tableWidget->rowCount()-1;
        connect(deleteButton, &QPushButton::clicked, this,[this, row]() {
                deleteRow(row);
            });


    }
    query.clear();
}
//主窗口显示
void MainWindow::showTables()
{
    for(int i=ui->tableWidget->rowCount()-1;i>=0;i--)
    {
        ui->tableWidget->removeRow(i);
    }
    ui->tableWidget->clear();
    if(table=="Contests"){
        showContestTables();
    }
    else if(table=="Scores")
    {
        showScoresTables();

    }else if(table=="Users")
    {
        showUsersTables();
    }
    if(table!="Scores")
    {
        for (int row = 0; row < ui->tableWidget->rowCount(); ++row)
        {
            QTableWidgetItem* item = ui->tableWidget->item(row, 0);
            if (item)
            {
                item->setFlags(item->flags() & ~Qt::ItemIsEditable);
            }
        }
    }else
    {
        for (int row = 0; row < ui->tableWidget->rowCount(); ++row)
        {
            QTableWidgetItem* item_1 = ui->tableWidget->item(row, 0);
            if (item_1)
            {
                item_1->setFlags(item_1->flags() & ~Qt::ItemIsEditable);
            }
            QTableWidgetItem* item_2 = ui->tableWidget->item(row, 1);
            if (item_2)
            {
                item_2->setFlags(item_2->flags() & ~Qt::ItemIsEditable);
            }
        }
    }
}
//查询按钮
void MainWindow::on_pushButton_clicked()
{

    QStringList items;
    QString str = ui->comboBox->currentText();
    if(str=="Contests")
    {
        items <<tr("contestid")<<tr("contestname")<<tr("time")<<tr("duration")<<tr("site");
        InputDialog inputDialog(str,items,this);
        QString item ;
        QString text ;

        if(inputDialog.exec()==QDialog::Accepted)
        {
            item = inputDialog.getItem();
            text = inputDialog.getText();
            for(int i=ui->tableWidget->rowCount()-1;i>=0;i--)
            {
                ui->tableWidget->removeRow(i);
            }
        }else return;
        QSqlQuery query=QSqlQuery(db);
        QString s;
        if(item=="contestid")
            s = "SELECT * FROM contests WHERE "+item+"="+text;
        else
            s = "SELECT * FROM contests WHERE "+item+" LIKE BINARY '%"+text+"%'";
        qDebug()<<s;
        query.exec(s);
        while(query.next())
        {
            int rowCount = ui->tableWidget->rowCount();
            ui->tableWidget->insertRow(rowCount);
            QString contestId=query.value("contestid").toString();
            QString contestName=query.value("contestname").toString();
            QString time = query.value("time").toDateTime().toString("yyyy-MM-dd hh:mm:ss");
            QString duration = query.value("duration").toTime().toString("hh:mm:ss");
            QString site = query.value("site").toString();
            ui->tableWidget->setItem(ui->tableWidget->rowCount()-1,0,new QTableWidgetItem(contestId));
            ui->tableWidget->setItem(ui->tableWidget->rowCount()-1,1,new QTableWidgetItem(contestName));
            ui->tableWidget->setItem(ui->tableWidget->rowCount()-1,2,new QTableWidgetItem(time));
            ui->tableWidget->setItem(ui->tableWidget->rowCount()-1,3,new QTableWidgetItem(duration));
            ui->tableWidget->setItem(ui->tableWidget->rowCount()-1,4,new QTableWidgetItem(site));
            QPushButton* deleteButton = new QPushButton("删除");
            ui->tableWidget->setCellWidget(ui->tableWidget->rowCount()-1,5, deleteButton);
            int row = ui->tableWidget->rowCount()-1;
            connect(deleteButton, &QPushButton::clicked, this,[this, row]() {
                    deleteRow(row);
                });

        }
        query.clear();


    }
    else if(str=="Users")
    {
        items <<tr("userid")<<tr("realname")<<tr("qq")<<tr("stuId")<<tr("codeforces")<<tr("missionid");
        InputDialog inputDialog(str,items,this);
        QString item ;
        QString text ;
        if(inputDialog.exec()==QDialog::Accepted)
        {
            item = inputDialog.getItem();
            text = inputDialog.getText();
            for(int i=ui->tableWidget->rowCount()-1;i>=0;i--)
            {
                ui->tableWidget->removeRow(i);
            }
        }else return;
        QSqlQuery query=QSqlQuery(db);
        QString s;
        if(item=="userid"||item == "missionid")
            s = "SELECT * FROM users WHERE "+item+"="+text;
        else
            s = "SELECT * FROM users WHERE "+item+" LIKE BINARY '%"+text+"%'";
        qDebug()<<s;
        query.exec(s);
        while(query.next())
        {
            int rowCount = ui->tableWidget->rowCount();
            ui->tableWidget->insertRow(rowCount);
            QString userId=query.value("userid").toString();
            QString realName=query.value("realname").toString();
            QString qq = query.value("qq").toString();
            QString stuId = query.value("stuid").toString();
            QString codeforces = query.value("codeforces").toString();
            QString missionId = query.value("missionid").toString();
            ui->tableWidget->setItem(ui->tableWidget->rowCount()-1,0,new QTableWidgetItem(userId));
            ui->tableWidget->setItem(ui->tableWidget->rowCount()-1,1,new QTableWidgetItem(realName));
            ui->tableWidget->setItem(ui->tableWidget->rowCount()-1,2,new QTableWidgetItem(qq));
            ui->tableWidget->setItem(ui->tableWidget->rowCount()-1,3,new QTableWidgetItem(stuId));
            ui->tableWidget->setItem(ui->tableWidget->rowCount()-1,4,new QTableWidgetItem(codeforces));
            ui->tableWidget->setItem(ui->tableWidget->rowCount()-1,5,new QTableWidgetItem(missionId));
            QPushButton* deleteButton = new QPushButton("删除");
            ui->tableWidget->setCellWidget(ui->tableWidget->rowCount()-1,6, deleteButton);
            int row = ui->tableWidget->rowCount()-1;
            connect(deleteButton, &QPushButton::clicked, this,[this, row]() {
                    deleteRow(row);
                });


        }
        query.clear();
    }

    else if(str=="Scores")
    {
        items <<tr("contestid")<<tr("userid")<<tr("rank")<<tr("number")<<tr("penalty");
        InputDialog inputDialog(str,items,this);
        QString item ;
        QString text ;
        if(inputDialog.exec()==QDialog::Accepted)
        {
            item = inputDialog.getItem();
            text = inputDialog.getText();
            for(int i=ui->tableWidget->rowCount()-1;i>=0;i--)
            {
                ui->tableWidget->removeRow(i);
            }
        }else return;
        QSqlQuery query=QSqlQuery(db);
        QString s;
        s = "SELECT * FROM scores WHERE "+item+"="+text;
        qDebug()<<s;
        query.exec(s);
        while(query.next())
        {
            int rowCount = ui->tableWidget->rowCount();
            ui->tableWidget->insertRow(rowCount);
            QString contestId=query.value("contestid").toString();
            QString userId=query.value("userid").toString();
            QString rank = query.value("rank").toString();
            QString number = query.value("number").toString();
            QString penalty = query.value("penalty").toString();
            ui->tableWidget->setItem(ui->tableWidget->rowCount()-1,0,new QTableWidgetItem(contestId));
            ui->tableWidget->setItem(ui->tableWidget->rowCount()-1,1,new QTableWidgetItem(userId));
            ui->tableWidget->setItem(ui->tableWidget->rowCount()-1,2,new QTableWidgetItem(rank));
            ui->tableWidget->setItem(ui->tableWidget->rowCount()-1,3,new QTableWidgetItem(number));
            ui->tableWidget->setItem(ui->tableWidget->rowCount()-1,4,new QTableWidgetItem(penalty));
            QPushButton* deleteButton = new QPushButton("删除");
            ui->tableWidget->setCellWidget(ui->tableWidget->rowCount()-1,5, deleteButton);
            int row = ui->tableWidget->rowCount()-1;
            connect(deleteButton, &QPushButton::clicked, this,[this, row]() {
                    deleteRow(row);
                });

        }
        query.clear();
    }

}

//添加按钮
void MainWindow::on_addPushButton_clicked()
{
    QStringList options;
    QString tableName = ui->comboBox->currentText();
    if(tableName=="Contests")
    {
        options<< "contestName" << "time(格式为:yyyy-MM-dd hh:mm:ss)" << "duration(格式为:hh:mm:ss)"<<"site";

        AddInputDialog addDialog(options,this);
        if(addDialog.exec()==QDialog::Accepted)
        {
            qDebug()<<"start Insert";

            QList<QString>inputs = addDialog.getInputs();
            if (inputs[0].isEmpty() || inputs[1].isEmpty() || inputs[2].isEmpty()||inputs[3].isEmpty()) {
                QMessageBox::warning(this, "警告", "输入不能为空！");
                return;
            }
            QSqlQuery query(db);
            query.prepare("INSERT INTO contests (contestname,time,duration,site) VALUES (?,?,?,?)");
            QString str=inputs[1];
            QDateTime datetime = QDateTime::fromString(str,"yyyy-MM-dd hh:mm:ss");
            QString str2=inputs[2];
            QTime time = QTime::fromString(str2,"hh:mm:ss");
            QString site = inputs[3];
            qDebug()<<inputs.at(0);
            qDebug()<<datetime;
            qDebug()<<time;
            qDebug()<<site;
            query.bindValue(0,inputs.at(0));
            query.bindValue(1,datetime);
            query.bindValue(2,time);
            query.bindValue(3,site);
            if (!datetime.isValid()) {
                // 转换失败，输入无效
                QMessageBox::warning(this, "警告", "无效的日期时间输入！");
                return;
            }
            if (!time.isValid()) {
                // 转换失败，输入无效
                QMessageBox::warning(this, "警告", "无效的时间输入！");
                return;
            }
            if(query.exec())
            {
                QMessageBox::information(this,"提示","添加成功！");
                showTables();
            }else
            {
                QMessageBox::information(this,"警告","添加失败!"+query.lastError().text());
            }

        }else return;
    }


    else if(tableName=="Scores")
    {
        options<< "contestid" << "userid" << "rank"<<"number"<<"penalty";


        AddInputDialog addDialog(options,this);
        if(addDialog.exec()==QDialog::Accepted)
        {
            qDebug()<<"start Insert";

            QList<QString>inputs = addDialog.getInputs();
            if (inputs[0].isEmpty() || inputs[1].isEmpty() || inputs[2].isEmpty()||inputs[3].isEmpty()||inputs[4].isEmpty()) {
                QMessageBox::warning(this, "警告", "输入不能为空！");
                return;
            }
            QSqlQuery query(db);
            query.prepare("INSERT INTO scores (contestid, userid, rank_pos, number, penalty) VALUES (?, ?, ?, ?, ?)");
            qDebug()<<inputs[0]<<" "<<inputs[1]
                              <<" "<<inputs[2]
                             <<" "<<inputs[3]
                            <<" "<<inputs[4];

            query.bindValue(0,inputs[0]);
            query.bindValue(1,inputs[1]);
            query.bindValue(2,inputs[2]);
            query.bindValue(3,inputs[3]);
            query.bindValue(4,inputs[4]);


            if(query.exec())
            {
                QMessageBox::information(this,"提示","添加成功！");
                showTables();
            }else
            {
                QMessageBox::information(this,"警告","添加失败!"+query.lastError().text());
            }

        }else return;
    }

    else if(tableName=="Users")
    {
        options<< "realname" << "qq" << "stuid"<<"codeforces"<<"missionid";

        AddInputDialog addDialog(options,this);
        if(addDialog.exec()==QDialog::Accepted)
        {
            qDebug()<<"start Insert";

            QList<QString>inputs = addDialog.getInputs();
            if (inputs[0].isEmpty() || inputs[1].isEmpty() || inputs[2].isEmpty()||inputs[3].isEmpty()||inputs[4].isEmpty()) {
                QMessageBox::warning(this, "警告", "输入不能为空！");
                return;
            }
            QSqlQuery query(db);
            query.prepare("INSERT INTO users (realname,qq,stuid,codeforces,missionid) VALUES (?,?,?,?,?)");

            query.bindValue(0,inputs.at(0));
            query.bindValue(1,inputs.at(1));
            query.bindValue(2,inputs.at(2));
            query.bindValue(3,inputs.at(3));
            query.bindValue(4,inputs.at(4));

            if(query.exec())
            {
                QMessageBox::information(this,"提示","添加成功！");
                showTables();
            }else
            {
                QMessageBox::information(this,"警告","添加失败!"+query.lastError().text());
            }

        }else return;
    }
}
//删除按钮
void MainWindow::deleteRow(int Row)
{
    qDebug()<<"clicked deleteRow"<<Row;
    int ret = QMessageBox::warning(this, "确认删除", "确定要删除选中的行吗？", QMessageBox::Yes | QMessageBox::No);
    if (ret == QMessageBox::No) {
        return;
    }
    QSqlQuery query(db);
    query.prepare("DELETE FROM "+ui->comboBox->currentText()+" where "+ui->tableWidget->horizontalHeaderItem(0)->text()+" = ?");
    query.addBindValue(ui->tableWidget->item(Row,0)->text());
    if(query.exec())
    {
        showTables();
    }else
    {
        QMessageBox::warning(this, "Error", "Failed to delete record: " + query.lastError().text());
    }
}

void MainWindow::onTableItemChanged(int row,int column)
{
    qDebug()<<row;
    qDebug()<<column;
    qDebug()<<table;
    QString id1,id2;
    QSqlQuery query(db);
    if(table=="Scores")
    {
        if(column==0||column==1)
        {
            return;
        }
        id1=ui->tableWidget->item(row,0)->text();
        id2=ui->tableWidget->item(row,1)->text();
        QString str = ui->tableWidget->item(row,column)->text();
        QString value = QInputDialog::getText(this, "编辑当前单元格", "请输入新的值：", QLineEdit::Normal, str);
        QString hd = ui->tableWidget->horizontalHeaderItem(column)->text();
        QString hd_1=ui->tableWidget->horizontalHeaderItem(0)->text();
        QString hd_2=ui->tableWidget->horizontalHeaderItem(1)->text();
        qDebug()<<hd;
        qDebug()<<value;
        qDebug()<<str;
        query.prepare("UPDATE "+table+" SET "+hd+" = ? (WHERE "+hd_1+" = ? AND "+hd_2+" = ?)");
        query.addBindValue(value);
        query.addBindValue(id1);
        query.addBindValue(id2);

        if(!query.exec())
        {
            QMessageBox::warning(this, "Error", "Failed to update record: " + query.lastError().text());
        }
    }else{
        if(column==0)
        {
            return;
        }
        id1=ui->tableWidget->item(row,0)->text();
        QString str = ui->tableWidget->item(row,column)->text();
        QString value = QInputDialog::getText(this, "编辑当前单元格", "请输入新的值：", QLineEdit::Normal, str);
        QString hd = ui->tableWidget->horizontalHeaderItem(column)->text();
        QString hd_=ui->tableWidget->horizontalHeaderItem(0)->text();
        qDebug()<<hd;
        qDebug()<<value;
        qDebug()<<str;
        query.prepare("UPDATE "+table+" SET "+hd+" = ? WHERE "+hd_+" = ? ");
        query.addBindValue(value);
        query.addBindValue(id1);

        if(!query.exec())
        {
            QMessageBox::warning(this, "Error", "Failed to update record: " + query.lastError().text());
        }
    }
    showTables();


}
