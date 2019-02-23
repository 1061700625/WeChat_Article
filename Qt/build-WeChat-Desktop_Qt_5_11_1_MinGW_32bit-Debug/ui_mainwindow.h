/********************************************************************************
** Form generated from reading UI file 'mainwindow.ui'
**
** Created by: Qt User Interface Compiler version 5.11.1
**
** WARNING! All changes made in this file will be lost when recompiling UI file!
********************************************************************************/

#ifndef UI_MAINWINDOW_H
#define UI_MAINWINDOW_H

#include <QtCore/QVariant>
#include <QtGui/QIcon>
#include <QtWidgets/QApplication>
#include <QtWidgets/QFormLayout>
#include <QtWidgets/QGridLayout>
#include <QtWidgets/QHBoxLayout>
#include <QtWidgets/QHeaderView>
#include <QtWidgets/QLabel>
#include <QtWidgets/QLineEdit>
#include <QtWidgets/QMainWindow>
#include <QtWidgets/QMenuBar>
#include <QtWidgets/QPushButton>
#include <QtWidgets/QSpacerItem>
#include <QtWidgets/QTableWidget>
#include <QtWidgets/QToolBar>
#include <QtWidgets/QVBoxLayout>
#include <QtWidgets/QWidget>

QT_BEGIN_NAMESPACE

class Ui_MainWindow
{
public:
    QWidget *centralWidget;
    QGridLayout *gridLayout;
    QHBoxLayout *horizontalLayout;
    QFormLayout *formLayout;
    QLabel *Label_target;
    QLineEdit *LineEdit_target;
    QLabel *Label_user;
    QLineEdit *LineEdit_user;
    QLabel *Label_pwd;
    QLineEdit *LineEdit_pwd;
    QLabel *gapLabel;
    QLineEdit *LineEdit_timegap;
    QSpacerItem *horizontalSpacer_2;
    QVBoxLayout *verticalLayout;
    QPushButton *pushButton_start;
    QPushButton *pushButton_stop;
    QSpacerItem *horizontalSpacer;
    QLabel *label_head;
    QLabel *label_notes;
    QTableWidget *tableWidget_result;
    QMenuBar *menuBar;
    QToolBar *mainToolBar;

    void setupUi(QMainWindow *MainWindow)
    {
        if (MainWindow->objectName().isEmpty())
            MainWindow->setObjectName(QStringLiteral("MainWindow"));
        MainWindow->setEnabled(true);
        MainWindow->resize(620, 520);
        QSizePolicy sizePolicy(QSizePolicy::Preferred, QSizePolicy::Preferred);
        sizePolicy.setHorizontalStretch(0);
        sizePolicy.setVerticalStretch(0);
        sizePolicy.setHeightForWidth(MainWindow->sizePolicy().hasHeightForWidth());
        MainWindow->setSizePolicy(sizePolicy);
        MainWindow->setMinimumSize(QSize(620, 520));
        MainWindow->setMouseTracking(false);
        QIcon icon;
        icon.addFile(QStringLiteral("../../Bingo.bmp"), QSize(), QIcon::Normal, QIcon::Off);
        MainWindow->setWindowIcon(icon);
        centralWidget = new QWidget(MainWindow);
        centralWidget->setObjectName(QStringLiteral("centralWidget"));
        gridLayout = new QGridLayout(centralWidget);
        gridLayout->setSpacing(6);
        gridLayout->setContentsMargins(11, 11, 11, 11);
        gridLayout->setObjectName(QStringLiteral("gridLayout"));
        horizontalLayout = new QHBoxLayout();
        horizontalLayout->setSpacing(6);
        horizontalLayout->setObjectName(QStringLiteral("horizontalLayout"));
        horizontalLayout->setSizeConstraint(QLayout::SetDefaultConstraint);
        formLayout = new QFormLayout();
        formLayout->setSpacing(6);
        formLayout->setObjectName(QStringLiteral("formLayout"));
        Label_target = new QLabel(centralWidget);
        Label_target->setObjectName(QStringLiteral("Label_target"));

        formLayout->setWidget(0, QFormLayout::LabelRole, Label_target);

        LineEdit_target = new QLineEdit(centralWidget);
        LineEdit_target->setObjectName(QStringLiteral("LineEdit_target"));
        LineEdit_target->setMinimumSize(QSize(200, 25));

        formLayout->setWidget(0, QFormLayout::FieldRole, LineEdit_target);

        Label_user = new QLabel(centralWidget);
        Label_user->setObjectName(QStringLiteral("Label_user"));
        Label_user->setLayoutDirection(Qt::LeftToRight);

        formLayout->setWidget(1, QFormLayout::LabelRole, Label_user);

        LineEdit_user = new QLineEdit(centralWidget);
        LineEdit_user->setObjectName(QStringLiteral("LineEdit_user"));
        LineEdit_user->setMinimumSize(QSize(200, 25));

        formLayout->setWidget(1, QFormLayout::FieldRole, LineEdit_user);

        Label_pwd = new QLabel(centralWidget);
        Label_pwd->setObjectName(QStringLiteral("Label_pwd"));

        formLayout->setWidget(2, QFormLayout::LabelRole, Label_pwd);

        LineEdit_pwd = new QLineEdit(centralWidget);
        LineEdit_pwd->setObjectName(QStringLiteral("LineEdit_pwd"));
        LineEdit_pwd->setMinimumSize(QSize(200, 25));
        LineEdit_pwd->setEchoMode(QLineEdit::Password);

        formLayout->setWidget(2, QFormLayout::FieldRole, LineEdit_pwd);

        gapLabel = new QLabel(centralWidget);
        gapLabel->setObjectName(QStringLiteral("gapLabel"));

        formLayout->setWidget(3, QFormLayout::LabelRole, gapLabel);

        LineEdit_timegap = new QLineEdit(centralWidget);
        LineEdit_timegap->setObjectName(QStringLiteral("LineEdit_timegap"));
        LineEdit_timegap->setMinimumSize(QSize(200, 25));

        formLayout->setWidget(3, QFormLayout::FieldRole, LineEdit_timegap);


        horizontalLayout->addLayout(formLayout);

        horizontalSpacer_2 = new QSpacerItem(30, 20, QSizePolicy::Expanding, QSizePolicy::Minimum);

        horizontalLayout->addItem(horizontalSpacer_2);

        verticalLayout = new QVBoxLayout();
        verticalLayout->setSpacing(6);
        verticalLayout->setObjectName(QStringLiteral("verticalLayout"));
        pushButton_start = new QPushButton(centralWidget);
        pushButton_start->setObjectName(QStringLiteral("pushButton_start"));
        pushButton_start->setMinimumSize(QSize(20, 50));
        pushButton_start->setCursor(QCursor(Qt::PointingHandCursor));
        pushButton_start->setIconSize(QSize(24, 24));

        verticalLayout->addWidget(pushButton_start);

        pushButton_stop = new QPushButton(centralWidget);
        pushButton_stop->setObjectName(QStringLiteral("pushButton_stop"));
        pushButton_stop->setMinimumSize(QSize(20, 50));
        pushButton_stop->setCursor(QCursor(Qt::PointingHandCursor));

        verticalLayout->addWidget(pushButton_stop);


        horizontalLayout->addLayout(verticalLayout);

        horizontalSpacer = new QSpacerItem(20, 20, QSizePolicy::Expanding, QSizePolicy::Minimum);

        horizontalLayout->addItem(horizontalSpacer);

        horizontalLayout->setStretch(0, 2);

        gridLayout->addLayout(horizontalLayout, 1, 0, 1, 1);

        label_head = new QLabel(centralWidget);
        label_head->setObjectName(QStringLiteral("label_head"));
        label_head->setMinimumSize(QSize(0, 120));

        gridLayout->addWidget(label_head, 0, 0, 1, 1);

        label_notes = new QLabel(centralWidget);
        label_notes->setObjectName(QStringLiteral("label_notes"));
        label_notes->setMinimumSize(QSize(0, 25));
        label_notes->setMaximumSize(QSize(16777215, 25));
        QFont font;
        font.setFamily(QString::fromUtf8("\345\215\216\346\226\207\346\245\267\344\275\223"));
        font.setPointSize(10);
        label_notes->setFont(font);
        label_notes->setAutoFillBackground(false);

        gridLayout->addWidget(label_notes, 2, 0, 1, 1);

        tableWidget_result = new QTableWidget(centralWidget);
        if (tableWidget_result->columnCount() < 2)
            tableWidget_result->setColumnCount(2);
        QTableWidgetItem *__qtablewidgetitem = new QTableWidgetItem();
        tableWidget_result->setHorizontalHeaderItem(0, __qtablewidgetitem);
        QTableWidgetItem *__qtablewidgetitem1 = new QTableWidgetItem();
        tableWidget_result->setHorizontalHeaderItem(1, __qtablewidgetitem1);
        if (tableWidget_result->rowCount() < 50)
            tableWidget_result->setRowCount(50);
        tableWidget_result->setObjectName(QStringLiteral("tableWidget_result"));
        QSizePolicy sizePolicy1(QSizePolicy::Expanding, QSizePolicy::Expanding);
        sizePolicy1.setHorizontalStretch(0);
        sizePolicy1.setVerticalStretch(0);
        sizePolicy1.setHeightForWidth(tableWidget_result->sizePolicy().hasHeightForWidth());
        tableWidget_result->setSizePolicy(sizePolicy1);
        tableWidget_result->viewport()->setProperty("cursor", QVariant(QCursor(Qt::IBeamCursor)));
        tableWidget_result->setAutoFillBackground(false);
        tableWidget_result->setFrameShape(QFrame::StyledPanel);
        tableWidget_result->setFrameShadow(QFrame::Sunken);
        tableWidget_result->setLineWidth(1);
        tableWidget_result->setMidLineWidth(1);
        tableWidget_result->setHorizontalScrollBarPolicy(Qt::ScrollBarAsNeeded);
        tableWidget_result->setSizeAdjustPolicy(QAbstractScrollArea::AdjustToContents);
        tableWidget_result->setAutoScroll(true);
        tableWidget_result->setAlternatingRowColors(true);
        tableWidget_result->setVerticalScrollMode(QAbstractItemView::ScrollPerPixel);
        tableWidget_result->setHorizontalScrollMode(QAbstractItemView::ScrollPerPixel);
        tableWidget_result->setGridStyle(Qt::SolidLine);
        tableWidget_result->setSortingEnabled(false);
        tableWidget_result->setRowCount(50);
        tableWidget_result->setColumnCount(2);
        tableWidget_result->horizontalHeader()->setProperty("showSortIndicator", QVariant(false));
        tableWidget_result->horizontalHeader()->setStretchLastSection(true);
        tableWidget_result->verticalHeader()->setCascadingSectionResizes(false);

        gridLayout->addWidget(tableWidget_result, 3, 0, 1, 1);

        MainWindow->setCentralWidget(centralWidget);
        menuBar = new QMenuBar(MainWindow);
        menuBar->setObjectName(QStringLiteral("menuBar"));
        menuBar->setGeometry(QRect(0, 0, 620, 23));
        MainWindow->setMenuBar(menuBar);
        mainToolBar = new QToolBar(MainWindow);
        mainToolBar->setObjectName(QStringLiteral("mainToolBar"));
        MainWindow->addToolBar(Qt::TopToolBarArea, mainToolBar);

        retranslateUi(MainWindow);
        QObject::connect(pushButton_start, SIGNAL(clicked()), MainWindow, SLOT(Start_Run()));
        QObject::connect(pushButton_stop, SIGNAL(clicked()), MainWindow, SLOT(Stop_Run()));

        QMetaObject::connectSlotsByName(MainWindow);
    } // setupUi

    void retranslateUi(QMainWindow *MainWindow)
    {
        MainWindow->setWindowTitle(QApplication::translate("MainWindow", "\345\276\256\344\277\241\345\205\254\344\274\227\345\217\267\346\226\207\347\253\240", nullptr));
        Label_target->setText(QApplication::translate("MainWindow", "\347\233\256\346\240\207\345\205\254\344\274\227\345\217\267\350\213\261\346\226\207\345\220\215", nullptr));
#ifndef QT_NO_STATUSTIP
        LineEdit_target->setStatusTip(QString());
#endif // QT_NO_STATUSTIP
        LineEdit_target->setPlaceholderText(QApplication::translate("MainWindow", "\344\270\272\347\251\272\345\210\231\351\273\230\350\256\244\346\226\260\345\215\216\347\244\276(xinhuashefabu1)", nullptr));
        Label_user->setText(QApplication::translate("MainWindow", "\344\270\252\344\272\272\345\205\254\344\274\227\345\217\267\350\264\246\345\217\267", nullptr));
        LineEdit_user->setPlaceholderText(QApplication::translate("MainWindow", "\344\270\272\347\251\272\345\210\231\350\207\252\345\212\250\346\211\223\345\274\200\351\241\265\351\235\242\345\220\216\346\211\213\345\212\250\350\276\223\345\205\245", nullptr));
        Label_pwd->setText(QApplication::translate("MainWindow", "\344\270\252\344\272\272\345\205\254\344\274\227\345\217\267\345\257\206\347\240\201", nullptr));
        LineEdit_pwd->setText(QString());
        LineEdit_pwd->setPlaceholderText(QApplication::translate("MainWindow", "\344\270\272\347\251\272\345\210\231\350\207\252\345\212\250\346\211\223\345\274\200\351\241\265\351\235\242\345\220\216\346\211\213\345\212\250\350\276\223\345\205\245", nullptr));
        gapLabel->setText(QApplication::translate("MainWindow", "\346\237\245\350\257\242\351\227\264\351\232\224(s)", nullptr));
        LineEdit_timegap->setPlaceholderText(QApplication::translate("MainWindow", "\344\270\272\347\251\272\345\210\231\351\273\230\350\256\244\344\270\27210s,\344\270\200\351\241\265\347\272\24610\346\235\241\357\274\214\350\266\212\347\237\255\350\266\212\345\277\253\350\242\253\351\231\220\345\210\266", nullptr));
        pushButton_start->setText(QApplication::translate("MainWindow", "\345\220\257\345\212\250(*^\342\226\275^*)", nullptr));
        pushButton_stop->setText(QApplication::translate("MainWindow", "\347\273\210\346\255\242\357\277\243\343\201\270\357\277\243", nullptr));
        label_head->setText(QApplication::translate("MainWindow", "****************************************************************************************************\n"
"* \347\250\213\345\272\217\345\216\237\347\220\206:\n"
">> \351\200\232\350\277\207selenium\347\231\273\345\275\225\350\216\267\345\217\226token\345\222\214cookie\357\274\214\345\206\215\350\207\252\345\212\250\347\210\254\345\217\226\345\222\214\344\270\213\350\275\275\n"
"* \344\275\277\347\224\250\345\211\215\346\217\220\357\274\232 *\n"
">> \347\224\265\350\204\221\345\267\262\350\243\205Firefox\343\200\201Chrome\343\200\201Opera\343\200\201Edge\347\255\211\346\265\217\350\247\210\345\231\250\n"
">> \344\270\213\350\275\275selenium\351\251\261\345\212\250\346\224\276\345\205\245python\345\256\211\350\243\205\347\233\256\345\275\225\357\274\214\345\260\206\347\233\256\345\275\225\346\267\273\345\212\240\350\207\263\347\216\257\345\242\203\345\217\230\351\207\217(https://www.seleniumhq.org/download/)\n"
">> \347\224\263\350\257\267\344\270\200\344\270\252\345\276\256\344\277\241\345\205\254\344\274\227\345"
                        "\217\267(https://mp.weixin.qq.com)\n"
"                         Copyright \302\251 SXF  \346\234\254\350\275\257\344\273\266\347\246\201\346\255\242\344\270\200\345\210\207\345\275\242\345\274\217\347\232\204\345\225\206\344\270\232\346\264\273\345\212\250\n"
"****************************************************************************************************", nullptr));
        label_notes->setText(QString());
        QTableWidgetItem *___qtablewidgetitem = tableWidget_result->horizontalHeaderItem(0);
        ___qtablewidgetitem->setText(QApplication::translate("MainWindow", "Title", nullptr));
        QTableWidgetItem *___qtablewidgetitem1 = tableWidget_result->horizontalHeaderItem(1);
        ___qtablewidgetitem1->setText(QApplication::translate("MainWindow", "URL", nullptr));
    } // retranslateUi

};

namespace Ui {
    class MainWindow: public Ui_MainWindow {};
} // namespace Ui

QT_END_NAMESPACE

#endif // UI_MAINWINDOW_H
